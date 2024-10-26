from .easybpy import *
import bpy.utils.previews
import os
from bpy.types import Scene, Menu, Operator
from bpy.utils import register_class, unregister_class
from bpy.props import (
    BoolProperty,
    FloatProperty,
    StringProperty,
    PointerProperty
)
# import botoes

_icons = None

bl_info = {
    "name": "Addon Janelas",
    "author": "Gabriel Gomides Surjus",
    "blender": (3, 3, 1),
    "version": (0, 0, 1),
    "location": "3D View",
    "description": "Descrição do meu add-on",
    "warning": "Beta Version",
    "site_url": "addonsblenderim.42web.io",
    "tracker_url": "addonsblenderim.42web.io",
    "support": "COMMUNITY",
    "category": "Generic"
}

# minhas Funçoes


def quantidadeDeObjetosNoBlendDiretorio(diretorio):
    src_path = diretorio

    with bpy.data.libraries.load(src_path) as (data_from, data_to):
        data_to.objects = data_from.objects

    cont = 0
    for obj in data_to.objects:
        cont += 1
    return cont


def importaAsset(diretorio, nomeAsset):
    src_path = diretorio

    with bpy.data.libraries.load(src_path) as (data_from, data_to):
        data_to.objects = data_from.objects

    for obj in data_to.objects:
        if (obj.name == nomeAsset):
            bpy.context.scene.collection.objects.link(obj)
            obj.location = bpy.context.scene.cursor.location

            nomeSplit = nomeAsset.split("_")
            nomeiaAsset(obj, nomeSplit[0])


def nomeiaAsset(objetoAtivo, nome):
    select_all_objects()
    todosOsObjetos = selected_objects()

    cont = 1
    for objeto in todosOsObjetos:
        nomeSplit = objeto.name.split("_")

        for split in range(len(nomeSplit)):
            if (nomeSplit[split].lower() == "windows"):
                cont = cont + 1

    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[objetoAtivo.name].select_set(True)
    rename_object(objetoAtivo, nome + "_" + str("%03d" % cont))
    bpy.context.view_layer.objects.active = objetoAtivo


def selecionaVertexGroup(numero):
    obj = bpy.context.object
    index = numero
    obj.vertex_groups.active_index = index


def redimencionaAsset(altura, largura):

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')

    cont = 0
    for cont in range(3):
        selecionaVertexGroup(cont)
        bpy.ops.object.vertex_group_select()

        if (cont == 0):
            bpy.ops.transform.translate(value=(largura/2, -0, -0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH',
                                        proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False)
        elif (cont == 1):
            bpy.ops.transform.translate(value=((-1*(largura/2)), -0, -0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH',
                                        proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'}, use_snap_project=False, snap_target='CLOSEST', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False)
        else:
            bpy.ops.transform.translate(value=(0, 0, altura), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH',
                                        proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'VERTEX'}, use_snap_project=False, snap_target='ACTIVE', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False)

        bpy.ops.mesh.select_all(action='DESELECT')

    bpy.ops.object.mode_set(mode='OBJECT')


def ajustarJanelaParaVeneziana(janela, alturaVeneziana):
    janela.vertex_groups.active_index = 2

    bpy.ops.object.select_all(action='DESELECT')

    bpy.context.view_layer.objects.active = janela

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')

    bpy.ops.object.vertex_group_select()

    bpy.ops.transform.translate(value=(0, 0, -alturaVeneziana), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH',
                                proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'VERTEX'}, use_snap_project=False, snap_target='ACTIVE', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False)

    bpy.ops.mesh.select_all(action='DESELECT')

    bpy.ops.object.mode_set(mode='OBJECT')


def removeVidro(janela):
    if bpy.context.object.mode != 'EDIT':
            set_edit_mode(janela)

    bpy.ops.mesh.select_all(action='DESELECT')
    materiais = get_materials_from_object(janela)

    for material in materiais:
        nameSplit = material.name.split(".")
        for rangeName in range(len(nameSplit)):
            if nameSplit[rangeName].lower() == "m_glass":
                 bpy.context.object.active_material_index = janela.material_slots.find(
                     material.name)
                 bpy.ops.object.material_slot_select()
                 bpy.ops.mesh.separate(type='SELECTED')

    set_object_mode(janela)

    objetosSelesionas = selected_objects()

    for objeto in objetosSelesionas:
        if objeto.name == janela.name + ".001":
            objeto.name = "Glass"
            objeto.parent = janela

def abreCanalLM(objeto):
    uv_layers = objeto.data.uv_layers
    key = False

    for uv_layer in uv_layers:
        if uv_layer.name == "LM":
            uv_layer.active = True
            key = True

        if(key):
            if bpy.context.object.mode != 'EDIT':
                set_edit_mode(objeto)
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.uv.select_all(action='SELECT')

            bpy.ops.uv.average_islands_scale()
            bpy.ops.uv.pack_islands()
                                
            bpy.context.scene.uvp2_props.pixel_margin = 8
            bpy.context.scene.uvp2_props.pixel_padding = 4
            bpy.context.scene.uvp2_props.pixel_margin_tex_size = 512
            bpy.ops.uv.average_islands_scale()
            bpy.ops.uvpackmaster2.uv_pack()       
        set_object_mode(objeto)
    
#-------------------------------------------------------------------
class AddWindowsSettings(bpy.types.PropertyGroup):
    blend_file: StringProperty(
        name="Diretório",
        description="Select the .blend file to import windows from",
        default="L:\Temp\\temp addon\Assets\janelas.blend",
        maxlen=1024,
        subtype="FILE_PATH"
    )

    height: FloatProperty(
        name="Altura",
        description="Height of the window in meters",
        default=0.0
    )

    width: FloatProperty(
        name="Largura",
        description="Width of the window in meters",
        default=0.0
    )    

#operadores

#Janelas
class AddWindowsButton(bpy.types.Operator):
    bl_label = "ADD_WINDOWS_BUTTON"
    bl_idname = "object.add_windows_button"
    bl_options = {'REGISTER', 'UNDO'}

    window: bpy.props.StringProperty()

    def execute(self, context):        
        bpy.ops.outliner.orphans_purge(do_recursive=True)
        
        splitName = "NULL"
        if (bpy.context.selected_objects):
            objetoSelecionado = bpy.context.active_object
            nomeObjetoAtivo = objetoSelecionado.name
            splitName = nomeObjetoAtivo.split("_")

        context = bpy.context
        # Verifica se o objeto está selecionado
        if(not bpy.context.selected_objects or splitName[0].lower() == "window"):
            if(splitName[0].lower() == "window"):
                delete_object()

            blend_file = bpy.path.abspath(context.scene.add_windows_settings.blend_file)
            print(blend_file)
            importaAsset(blend_file, self.window)
            
            redimencionaAsset(context.scene.add_windows_settings.width, context.scene.add_windows_settings.height)
                
            quantidadeDeObjetosNoBlendDiretorio(blend_file)

            janela = bpy.context.active_object
            #removeVidro(janela)
            abreCanalLM(janela)
            
            bpy.ops.outliner.orphans_purge(do_recursive=True)

        else:
            self.report({'ERROR'}, "Janela não selecionada")         
            
        return {'FINISHED'}
    
#Venezianas
class AddVenezianasButton01(bpy.types.Operator):
    bl_label = "ADD_VENEZIANAS_BUTTON_01"
    bl_idname = "object.add_venezianas_button_01"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
              
        objetoSelecionado = bpy.context.active_object        
        nomeObjetoAtivo = objetoSelecionado.name
        splitName = nomeObjetoAtivo.split("_")
        
        
        if(splitName[0].lower() == "window" and objetoSelecionado is not None and objetoSelecionado.select_get()):
            janelaSelecionada = objetoSelecionado
            dimensionsJanela = janelaSelecionada.dimensions
            larguraJanela = dimensionsJanela.x
            alturaJanela = dimensionsJanela.z
            
            blend_file = bpy.path.abspath(context.scene.add_windows_settings.blend_file)
            importaAsset(blend_file, "Venezianas_01")
            
            redimencionaAsset(0, larguraJanela)
            
            #posicionar veneziana
            venezianaSelecionado = bpy.context.active_object
            dimensionsVeneziana = venezianaSelecionado.dimensions
            alturaVeneziana = dimensionsVeneziana.z
            bpy.ops.transform.translate(value=(0, 0, alturaJanela - alturaVeneziana), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, snap=False, snap_elements={'VERTEX'}, use_snap_project=False, snap_target='ACTIVE', use_snap_self=False, use_snap_edit=False, use_snap_nonedit=False, use_snap_selectable=False)

            #ajusta a janela
            ajustarJanelaParaVeneziana(janelaSelecionada, alturaVeneziana)
            
            bpy.data.objects[venezianaSelecionado.name].select_set(True)
            bpy.data.objects[janelaSelecionada.name].select_set(True)
            bpy.context.view_layer.objects.active = janelaSelecionada
            
            bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)

        
        else:
            self.report({'ERROR'}, "Janela não selecionada")      
        
        bpy.ops.outliner.orphans_purge(do_recursive=True)
        
            
        return {'FINISHED'}


class ImportAssetsButton(bpy.types.Operator):
    bl_label = "IMPORT_ASSETS_BUTTON"
    bl_idname = "object.import_assets_button"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        blend_file = bpy.path.abspath(context.scene.add_windows_settings.blend_file)
        
        quantidadeDeJanelas = quantidadeDeObjetosNoBlendDiretorio(blend_file)
        
        print(quantidadeDeJanelas)
        
        return {'FINISHED'}
    
# PANEL UI
class PanelPrincipal(bpy.types.Panel):
    bl_label = 'Panel principal'
    bl_idname = 'OBJECT_PT_panel_principal'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'Janelas IM'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        
        scene = context.scene
        settings = scene.add_windows_settings        

        # Import Assets button
        row = layout.row()
        row.prop(settings, "blend_file", text="Diretório")
        
        row = layout.row()
        row.operator("object.import_assets_button", text="Importar", icon="IMPORT")

def create_window_button(layout, icon_name, window_name):
    box = layout.box()
    box.alert = False
    box.enabled = True
    box.active = True
    box.use_property_split = False
    box.use_property_decorate = False
    box.alignment = 'Expand'.upper()
    box.scale_x = 1.0
    box.scale_y = 1.0
    box.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row = layout.row()
    box.template_icon(icon_value=_icons[icon_name].icon_id, scale=5.00)
    row = layout.row()       
    box.operator("object.add_windows_button", text=window_name, icon="WINDOW").window = window_name
    
class AddWindowsPanel(bpy.types.Panel):
    bl_label = "Add Windows"
    bl_idname = "OBJECT_PT_add_windows_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tools"
    bl_parent_id = "OBJECT_PT_panel_principal"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        settings = scene.add_windows_settings        
        
        # Windows settings        
        box01 = layout.box()
        box01.alert = False
        box01.enabled = True
        box01.active = True
        box01.use_property_split = False
        box01.use_property_decorate = False
        box01.alignment = 'Expand'.upper()
        box01.scale_x = 1.0
        box01.scale_y = 1.0
        box01.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row = layout.row()         
        box01.prop(settings, "height", text="Largura")
        box01.prop(settings, "width", text="Altura")
        
        row.label(text="Windows")

         # Add Windows button
        create_window_button(layout, 'Window_01.png', 'Window_01')
        create_window_button(layout, 'Window_02.png', 'Window_02')
        create_window_button(layout, 'Window_03.png', 'Window_03')
        create_window_button(layout, 'Window_04.png', 'Window_04')
        create_window_button(layout, 'Window_05.png', 'Window_05')
        create_window_button(layout, 'Window_06.png', 'Window_06')
        create_window_button(layout, 'Window_07.png', 'Window_07')
        create_window_button(layout, 'Window_08.png', 'Window_08')
        create_window_button(layout, 'Window_09.png', 'Window_09')
        create_window_button(layout, 'Window_10.png', 'Window_10')
        create_window_button(layout, 'Window_11.png', 'Window_11')
        create_window_button(layout, 'Window_12.png', 'Window_12')
        create_window_button(layout, 'Window_13.png', 'Window_13')
        create_window_button(layout, 'Window_14.png', 'Window_14')
        create_window_button(layout, 'Window_14.png', 'Window_15')       
        
classes = (
    PanelPrincipal,
    ImportAssetsButton,
    AddWindowsPanel,
    AddWindowsSettings,
    AddWindowsButton,
    AddVenezianasButton01
)

def register():
    global _icons
    _icons = bpy.utils.previews.new()
    if not 'Window_01.png' in _icons: _icons.load('Window_01.png', os.path.join(os.path.dirname(__file__), 'icons', 'Window_01.png'), "IMAGE")
    if not 'Window_02.png' in _icons: _icons.load('Window_02.png', os.path.join(os.path.dirname(__file__), 'icons', 'Window_02.png'), "IMAGE")
    if not 'Window_03.png' in _icons: _icons.load('Window_03.png', os.path.join(os.path.dirname(__file__), 'icons', 'Window_03.png'), "IMAGE")
    if not 'Window_04.png' in _icons: _icons.load('Window_04.png', os.path.join(os.path.dirname(__file__), 'icons', 'Window_04.png'), "IMAGE")
    if not 'Window_05.png' in _icons: _icons.load('Window_05.png', os.path.join(os.path.dirname(__file__), 'icons', 'Window_05.png'), "IMAGE")
    if not 'Window_06.png' in _icons: _icons.load('Window_06.png', os.path.join(os.path.dirname(__file__), 'icons', 'Window_06.png'), "IMAGE")
    if not 'Window_07.png' in _icons: _icons.load('Window_07.png', os.path.join(os.path.dirname(__file__), 'icons', 'Window_07.png'), "IMAGE")
    if not 'Window_08.png' in _icons: _icons.load('Window_08.png', os.path.join(os.path.dirname(__file__), 'icons', 'Window_08.png'), "IMAGE")
    if not 'Window_09.png' in _icons: _icons.load('Window_09.png', os.path.join(os.path.dirname(__file__), 'icons', 'Window_09.png'), "IMAGE")
    if not 'Window_10.png' in _icons: _icons.load('Window_10.png', os.path.join(os.path.dirname(__file__), 'icons', 'Window_10.png'), "IMAGE")
    if not 'Window_11.png' in _icons: _icons.load('Window_11.png', os.path.join(os.path.dirname(__file__), 'icons', 'Window_11.png'), "IMAGE")
    if not 'Window_12.png' in _icons: _icons.load('Window_12.png', os.path.join(os.path.dirname(__file__), 'icons', 'Window_12.png'), "IMAGE")
    if not 'Window_13.png' in _icons: _icons.load('Window_13.png', os.path.join(os.path.dirname(__file__), 'icons', 'Window_13.png'), "IMAGE")
    if not 'Window_14.png' in _icons: _icons.load('Window_14.png', os.path.join(os.path.dirname(__file__), 'icons', 'Window_14.png'), "IMAGE")
    if not 'Window_15.png' in _icons: _icons.load('Window_15.png', os.path.join(os.path.dirname(__file__), 'icons', 'Window_15.png'), "IMAGE")    
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.add_windows_settings = PointerProperty(type=AddWindowsSettings)
    

def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)    
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.add_windows_settings
    

if __name__ == "__main__":
    register()
