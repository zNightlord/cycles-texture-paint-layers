'''
Copyright (C) 2018 DAVID DIGIOIA
DAVIDOFJOY@GMAIL.com

Created by DAVID DIGIOIA

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Layers",
    "description": "Layer functionality using nodes for texture paint",
    "author": "David DiGioia, Alexander Belyakov",
    "version": (0, 0, 2),
    "blender": (2, 80, 0),
    "location": "View3D > Tool > Layers",
    "warning": "This addon is still in development.",
    "wiki_url": "",
    "category": "Paint"
}


import bpy
from .data.layer_data import Layer
from .data.layer_img_data import LayerImgData
from .data.layer_shader_data import LayerShaders
from .operators.delete_layer import LAYER_OT_dellayer
from .operators.move_layer import LAYER_OT_movelayer
from .operators.new_layer import LAYER_OT_newlayer
from .operators.merge_visible_layers import MergeVisibleLayers
from .ui.layer_list import MATERIAL_UL_layerlist
from .ui.layer_panel import LAYER_PT_panel

classes = (
    Layer,
    LayerImgData,
    LayerShaders,
    LAYER_OT_dellayer,
    LAYER_OT_movelayer,
    LAYER_OT_newlayer,
    MergeVisibleLayers,
    MATERIAL_UL_layerlist,
    LAYER_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    def get_index(self):
        return self.layer_private_index

    def set_index(self, index):
        layer_list = bpy.context.object.active_material.layer_list

        if index < 0 or index >= len(layer_list):
            self.layer_private_index = index
            return

        layer = bpy.context.object.active_material.layer_list[index]
        img_name = layer.texture

        # Need to update scene in order for slots to update in time
        layer = bpy.context.view_layer
        layer.update()

        slots = bpy.context.object.active_material.texture_paint_images
        slot_index = None
        for i, slot in enumerate(slots):
            if slot.name == img_name:
                slot_index = i
        try:
            bpy.context.object.active_material.paint_active_slot = slot_index
        except TypeError as e:
            print("No slot names match layer name. There are probably missing slots")
            print("Error: " + str(e))
        self.layer_private_index = index

    bpy.types.Material.layer_list = bpy.props.CollectionProperty(type=Layer)
    bpy.types.Material.layer_index = bpy.props.IntProperty(name="Index for layer list", default=0, get=get_index, set=set_index)
    bpy.types.Material.layer_private_index = bpy.props.IntProperty(name="PRIVATE layer index", default=0)
    bpy.types.Material.layer_shaders = bpy.props.PointerProperty(type=LayerShaders)
    bpy.types.Material.layer_img_data = bpy.props.PointerProperty(type=LayerImgData)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Material.layer_list
    del bpy.types.Material.layer_index
    del bpy.types.Material.layer_private_index
    del bpy.types.Material.layer_shaders
    del bpy.types.Material.layer_img_data
