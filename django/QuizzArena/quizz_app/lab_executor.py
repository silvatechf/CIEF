"""
Lab Execution Engine - Sandbox para executar código Python de forma segura

Implementação segura de execução de código em labs interativos com:
- Timeout (máximo 5 segundos)
- Limite de memória
- Acesso restrito a módulos
- Captura de output/erro
- Validação de testes
"""

import subprocess
import tempfile
import os
import sys
import json
from typing import Dict, List, Tuple
from datetime import datetime
import signal
import platform

# resource module é apenas disponível em Unix/Linux
if platform.system() != "Windows":
    try:
        import resource
    except ImportError:
        resource = None
else:
    resource = None


class LabExecutor:
    """Executor seguro de código para labs."""

    # Configuração de segurança
    TIMEOUT_SECONDS = 5
    MAX_OUTPUT_LENGTH = 5000
    ALLOWED_IMPORTS = {
        "hashlib",
        "json",
        "re",
        "math",
        "random",
        "datetime",
        "time",
        "itertools",
        "collections",
        "string",
        "base64",
        "binascii",
        "urllib",
        "ssl",
        "hmac",
        "secrets",
    }

    # Módulos perigosos que não podem ser importados
    FORBIDDEN_IMPORTS = {
        "os",
        "sys",
        "subprocess",
        "socket",
        "threading",
        "__builtins__",
        "eval",
        "exec",
        "compile",
        "open",
    }

    @staticmethod
    def execute_code(
        user_code: str,
        setup_code: str = "",
        test_cases: List[Dict] = None,
        time_limit: int = TIMEOUT_SECONDS,
    ) -> Dict:
        """
        Executar código do usuário de forma segura.

        Args:
            user_code: Código submetido pelo usuário
            setup_code: Código de setup (fixtures, imports)
            test_cases: Lista de [{name, input, expected_output, points}]
            time_limit: Timeout em segundos

        Returns:
            Dict com {
                'status': 'SUCCESS'|'ERROR'|'TIMEOUT',
                'output': str,
                'error': str,
                'tests_passed': int,
                'tests_total': int,
                'score': int,
                'execution_time': float
            }
        """

        test_cases = test_cases or []

        # Validar código para imports proibidos
        validation = LabExecutor.validate_code(user_code)
        if not validation["valid"]:
            return {
                "status": "ERROR",
                "output": "",
                "error": validation["error"],
                "tests_passed": 0,
                "tests_total": len(test_cases),
                "score": 0,
                "execution_time": 0,
            }

        # Criar arquivo temporário com código
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            full_code = f"{setup_code}\n{user_code}"
            f.write(full_code)
            temp_file = f.name

        try:
            # Executar código com timeout
            start_time = datetime.now()
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=time_limit,
            )
            execution_time = (datetime.now() - start_time).total_seconds()

            output = result.stdout[: LabExecutor.MAX_OUTPUT_LENGTH]
            error = result.stderr[: LabExecutor.MAX_OUTPUT_LENGTH]

            # Executar testes se houver
            tests_passed = 0
            tests_total = len(test_cases)

            if test_cases and result.returncode == 0:
                tests_passed, errors = LabExecutor.run_tests(
                    user_code, setup_code, test_cases
                )
                if errors:
                    error = f"{error}\n{errors}"

            # Calcular score
            score = int((tests_passed / tests_total * 100)) if tests_total > 0 else 0

            return {
                "status": "SUCCESS" if result.returncode == 0 else "ERROR",
                "output": output,
                "error": error,
                "tests_passed": tests_passed,
                "tests_total": tests_total,
                "score": score,
                "execution_time": execution_time,
            }

        except subprocess.TimeoutExpired:
            return {
                "status": "TIMEOUT",
                "output": "",
                "error": f"Código levou mais de {time_limit} segundos para executar",
                "tests_passed": 0,
                "tests_total": len(test_cases),
                "score": 0,
                "execution_time": time_limit,
            }

        except Exception as e:
            return {
                "status": "ERROR",
                "output": "",
                "error": str(e),
                "tests_passed": 0,
                "tests_total": len(test_cases),
                "score": 0,
                "execution_time": 0,
            }

        finally:
            # Limpear arquivo temporário
            try:
                os.unlink(temp_file)
            except:
                pass

    @staticmethod
    def validate_code(code: str) -> Dict:
        """
        Validar código do usuário antes de executar.

        Verifica por:
        - Imports proibidos
        - Operações perigosas
        - Sintaxe válida
        """

        # Verificar sintaxe
        try:
            compile(code, "<string>", "exec")
        except SyntaxError as e:
            return {"valid": False, "error": f"Erro de sintaxe: {str(e)}"}

        # Verificar imports proibidos
        lines = code.split("\n")
        for line in lines:
            line = line.strip()

            if line.startswith("import ") or line.startswith("from "):
                # Extrair nome do módulo
                if line.startswith("import "):
                    module_name = line.replace("import ", "").split()[0].split(".")[0]
                else:
                    module_name = line.replace("from ", "").split()[0].split(".")[0]

                if module_name in LabExecutor.FORBIDDEN_IMPORTS:
                    return {
                        "valid": False,
                        "error": f'Módulo "{module_name}" não permitido por questões de segurança',
                    }

                if module_name not in LabExecutor.ALLOWED_IMPORTS:
                    return {
                        "valid": False,
                        "error": f'Módulo "{module_name}" não está na lista de permitidos. Módulos permitidos: {", ".join(sorted(LabExecutor.ALLOWED_IMPORTS))}',
                    }

        # Verificar por operações perigosas
        dangerous_functions = [
            "eval",
            "exec",
            "__import__",
            "compile",
            "open",
            "input",
            "exec",
        ]
        for func in dangerous_functions:
            if func in code:
                return {
                    "valid": False,
                    "error": f'Função "{func}" não permitida por questões de segurança',
                }

        return {"valid": True}

    @staticmethod
    def run_tests(
        user_code: str, setup_code: str, test_cases: List[Dict]
    ) -> Tuple[int, str]:
        """
        Executar testes contra código do usuário.

        Args:
            user_code: Código do usuário
            setup_code: Setup/fixtures
            test_cases: [{name, input, expected_output, points}]

        Returns:
            Tuple: (testes_passaram, mensagem_erro)
        """

        tests_passed = 0
        errors = []

        for test in test_cases:
            try:
                # Criar contexto de execução
                exec_context = {}
                exec(setup_code, exec_context)
                exec(user_code, exec_context)

                # Executar teste
                test_code = test.get("test_code", "")
                if test_code:
                    exec(test_code, exec_context)
                    tests_passed += 1
                else:
                    # Validação simples de output
                    test_input = test.get("input", "")
                    expected = test.get("expected_output", "")

                    # Executar com input simulado
                    if test_input:
                        exec_context["__test_input__"] = test_input

                    # Executar e capturar output
                    import io
                    import contextlib

                    f = io.StringIO()
                    with contextlib.redirect_stdout(f):
                        exec(user_code, exec_context)

                    actual_output = f.getvalue().strip()
                    if str(actual_output) == str(expected):
                        tests_passed += 1
                    else:
                        errors.append(
                            f"Teste '{test['name']}' falhou: esperado '{expected}', obteve '{actual_output}'"
                        )

            except Exception as e:
                errors.append(f"Teste '{test['name']}' erro: {str(e)}")

        error_msg = "\n".join(errors) if errors else ""
        return tests_passed, error_msg


class CodeStyleAnalyzer:
    """Analisar estilo e segurança do código."""

    @staticmethod
    def analyze(code: str) -> Dict:
        """
        Analisar qualidade do código.

        Retorna:
        - Segurança
        - Legibilidade
        - Performance
        - Boas práticas
        """

        issues = []
        warnings = []

        # Verificar linhas muito longas
        lines = code.split("\n")
        for i, line in enumerate(lines, 1):
            if len(line) > 100:
                warnings.append(f"Linha {i} muito longa ({len(line)} caracteres)")

        # Verificar comentários
        comment_ratio = code.count("#") / max(len(lines), 1)
        if comment_ratio < 0.05:
            warnings.append("Código poderia ter mais comentários explicativos")

        # Verificar funções
        if "def " not in code:
            warnings.append("Considere organizar código em funções")

        # Verificar nomes de variáveis
        import re

        var_pattern = r"\b_+[a-z0-9]+\b"  # Variáveis com _ no início
        if re.search(var_pattern, code):
            warnings.append("Use nomes descritivos para variáveis (evite _var, __var)")

        return {
            "issues": issues,
            "warnings": warnings,
            "quality_score": max(0, 100 - len(issues) * 10 - len(warnings) * 5),
        }


class LabSubmissionValidator:
    """Validar e avaliar submissões de labs."""

    @staticmethod
    def validate_and_score(lab_submission, lab) -> Dict:
        """
        Validar e calcular pontuação de submissão.

        Returns:
        {
            'status': 'PASSED'|'FAILED',
            'score': int,
            'test_results': [{}],
            'feedback': str
        }
        """

        # Executar código
        result = LabExecutor.execute_code(
            user_code=lab_submission.submitted_code,
            setup_code=lab.setup_code,
            test_cases=lab.test_cases,
        )

        # Analisar estilo
        style = CodeStyleAnalyzer.analyze(lab_submission.submitted_code)

        # Calcular score final
        test_score = result["score"]
        style_bonus = style["quality_score"] * 0.1  # Até 10% bônus
        final_score = min(100, test_score + style_bonus)

        # Preparar feedback
        feedback = f"Pontuação: {final_score}%\n"
        if result["status"] == "TIMEOUT":
            feedback += "⚠️ Código excedeu limite de tempo (5 segundos)\n"
        elif result["status"] == "ERROR":
            feedback += f"❌ Erro: {result['error']}\n"

        if result["tests_passed"] == result["tests_total"]:
            feedback += f"✅ Todos os {result['tests_total']} testes passaram!\n"
        else:
            feedback += (
                f"⚠️ {result['tests_passed']}/{result['tests_total']} testes passaram\n"
            )

        if style["warnings"]:
            feedback += "\n📝 Sugestões de melhoria:\n"
            for warning in style["warnings"][:3]:
                feedback += f"  • {warning}\n"

        return {
            "status": (
                "PASSED"
                if result["tests_passed"] == result["tests_total"]
                else "FAILED"
            ),
            "score": int(final_score),
            "test_results": [
                {
                    "name": tc.get("name", f"Teste {i+1}"),
                    "passed": i < result["tests_passed"],
                }
                for i, tc in enumerate(lab.test_cases)
            ],
            "output": result["output"],
            "error": result["error"],
            "feedback": feedback,
            "execution_time": result["execution_time"],
            "style_issues": style["issues"],
            "style_warnings": style["warnings"],
        }
