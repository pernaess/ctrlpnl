from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from ctrlpnl.forms import CtrlpnlForm

class CtrlpnlView(TemplateView):
    template_name = 'ctrlpnl/ctrlpnl.html'

    def get(self, request):
        form = CtrlpnlForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CtrlpnlForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['post']
            return redirect('ctrlpnl:ctrlpnl')

        args = {'form': form, 'text': text}
        return render(request, self.template_name, args)
