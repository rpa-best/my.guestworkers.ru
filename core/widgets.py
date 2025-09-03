from unfold.contrib.forms.widgets import ArrayWidget


class ReadOnlyArrayWidget(ArrayWidget):
    template_name = 'core/readonly_array.html'
