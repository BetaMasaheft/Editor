from django import forms

class StandardCharField():

    def __init__(self, name, xpath, mode):
        self.name = name
        self.xpath = xpath
        self.mode = mode
        self.field_class = forms.CharField

    def create_and_initialise(ft):
        xpath_node = ft.ns_xpath(self.xpath)
        return CharField(initial=xpath_node) 

def append(element, text_function):
    """Appends the results of at text generation function to an element. 

    :element: TODO
    :text_function: TODO
    :returns: TODO

    """
    return 

def replace(element, text_function):
    """Replaces an element with the result of a text generation function.

    :element: TODO
    :text_function: TODO
    :returns: TODO

    """
    return 

EDIT_ACTION_FUNCTIONS = (
        (append, "append"),
        (replace, "replace")
        )
