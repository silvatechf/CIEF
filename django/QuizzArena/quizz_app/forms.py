from django import forms

class CyberSecQuizForm(forms.Form):
    def __init__(self, *args, questions=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        if questions:
            for question in questions:
                field_name = f'question_{question.id}'
                
                # Monta as opções dinamicamente do JSONField
                choices = []
                if isinstance(question.options, list):
                    choices = [(idx, opt) for idx, opt in enumerate(question.options)]
                elif isinstance(question.options, dict):
                    choices = [(k, v) for k, v in question.options.items()]
                
                self.fields[field_name] = forms.ChoiceField(
                    label=question.content,
                    choices=choices,
                    widget=forms.RadioSelect(attrs={'class': 'quiz-radio'}),
                    required=True,
                    error_messages={'required': 'Por favor, selecione uma resposta.'}
                )