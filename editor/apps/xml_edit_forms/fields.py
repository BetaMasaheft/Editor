from django import forms

class StandardCharField():

    def __init__(self, name, xpath, mode):
        self.name = name
        self.xpath = xpath
        self.mode = mode
        self.field_class = forms.CharField

    def initialise_field(self, typed_file):
        xpath_node = typed_file.ns_xpath(self.xpath)
        return self.name, self.field_class(initial=xpath_node)

    def process_field(self, typed_file):

        return typed_file

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
