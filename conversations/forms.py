from django import forms


# 이 form 은 안 쓰이고 있음. 그냥 conversation_detail 에서 naked input 으로 활용중
class AddCommentForm(forms.Form):

    message = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "Add a Comment"})
    )