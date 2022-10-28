"""
This module is an example of a barebones QWidget plugin for napari

It implements the Widget specification.
see: https://napari.org/stable/plugins/guides.html?#widgets

Replace code below according to your needs.
"""
from typing import TYPE_CHECKING

from magicgui import magic_factory
from qtpy.QtWidgets import QHBoxLayout, QPushButton, QWidget

if TYPE_CHECKING:
    import napari


class ExampleQWidget(QWidget):
    # your QWidget.__init__ can optionally request the napari viewer instance
    # in one of two ways:
    # 1. use a parameter called `napari_viewer`, as done here
    # 2. use a type annotation of 'napari.viewer.Viewer' for any parameter
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer

        btn = QPushButton("Click me!")
        btn.clicked.connect(self._on_click)

        self.setLayout(QHBoxLayout())
        self.layout().addWidget(btn)

    def _on_click(self):
        print("napari has", len(self.viewer.layers), "layers")


@magic_factory
def example_magic_widget(img_layer: "napari.layers.Image"):
    print(f"you have selected {img_layer}")


# Uses the `autogenerate: true` flag in the plugin manifest
# to indicate it should be wrapped as a magicgui to autogenerate
# a widget.
def example_function_widget(img_layer: "napari.layers.Image"):
    print(f"you have selected {img_layer}")
    

    
import napari
from magicgui import magicgui
from magicgui import widgets
import pathlib
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    # your plugin doesn't need to import napari at all just to use these types
    # just put these imports here and wrap the hints in quotes
    import napari.types
    import napari.viewer

    
@magicgui(
    call_button='Add Image',
    file_directory = dict(widget_type = 'FileEdit', mode = 'd', label = 'Select Directory'),
    search_field = dict(widget_type = 'LineEdit', label = 'File Type'),
    file_select = dict(widget_type = 'Select', label = 'Choose File')
)
def folder_explorer(
    viewer: 'napari.viewer.Viewer',
    file_directory= pathlib.Path(),
    search_field = '*.czi',
    file_select = []
):
    viewer.open(file_select, plugin = 'napari-aicsimageio')

@folder_explorer.file_directory.changed.connect
def _update_file_select(file_directory):
    choices = list(file_directory.glob(pattern=folder_explorer.search_field.value))
    folder_explorer.file_select.choices = choices

