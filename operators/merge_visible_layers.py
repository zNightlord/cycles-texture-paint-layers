import bpy


class MergeVisibleLayers(bpy.types.Operator):
    bl_idname = "merge.visible_layers"
    bl_label = "Merge visible layers"
    bl_description = "Merge visible layers into single image"
    bl_options = {"REGISTER"}

    def execute(self, context):
        # Store current scene settings
        scene = context.scene
        render_engine = scene.render.engine
        samples = scene.cycles.samples
        bake_type = scene.cycles.bake_type
        pass_direct = scene.render.bake.use_pass_direct
        pass_indirect = scene.render.bake.use_pass_indirect

        # Bake layers
        img_data = context.object.active_material.layer_img_data
        img = bpy.data.images.new(name="merged_layers", alpha=True, width=img_data.width,
                                  height=img_data.height, float_buffer=img_data.bit_depth)

        mat = bpy.context.object.active_material
        current_active_node = mat.node_tree.nodes.active
        nodes = mat.node_tree.nodes
        node_texture = nodes.new(type="ShaderNodeTexImage")
        nodes.active = node_texture
        node_texture.image = img

        scene.render.engine = 'CYCLES'
        scene.cycles.samples = 1
        scene.cycles.bake_type = 'DIFFUSE'
        scene.render.bake.use_pass_direct = False
        scene.render.bake.use_pass_indirect = False
        scene.bake.use_pass_color = True
        bpy.ops.object.bake(type='DIFFUSE')

        nodes.remove(node_texture)

        # Restore settings
        scene.render.engine = render_engine
        scene.cycles.samples = samples
        scene.cycles.bake_type = bake_type
        scene.render.bake.use_pass_direct = pass_direct
        scene.render.bake.use_pass_indirect = pass_indirect
        nodes.active = current_active_node
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=130)

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        cbk = scene.render.bake

        layout.prop(cbk, "margin")
        layout.separator()
