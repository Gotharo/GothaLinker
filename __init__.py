try:
    import bpy
except ImportError:
    print("Warning: bpy module not found. This script must be run inside Blender.")
    
bl_info = {
    "name": "GothaLinker",
    "description": "Animar y mejorar animaciones desed shape keys",
    "author": "Gonzalo Castro (Gotharo)",
    "version": (2, 4),
    "blender": (4, 2),
    "category": "Object",
}

# Aligner Tool
from .Align_bone_empty import CopyTransformsOperator, update_list, register as align_register, unregister as align_unregister

# Propiedades para los inputs
bpy.types.Scene.target_dropdown = bpy.props.EnumProperty(
    name="Target",
    description="Selecciona el Target",
    items=update_list
)

bpy.types.Scene.object_dropdown = bpy.props.EnumProperty(
    name="Object",
    description="Selecciona el Object",
    items=update_list
)



# Libreria para BlendShapes

from .Phon_config import phoneme_configs
from .Phon_config import control_pairs
from .Phon_config import objetos_brows
from .Phon_config import objetos_mid_Head
from .Phon_config import objetos_mouth_jaw

def seleccionar_huesos_left_hand():
    """Selecciona los huesos de la mano izquierda en el armature seleccionado."""
    left_hand_bones = [
        "c_pinky1_base.l", "c_pinky1.l", "c_pinky2.l", "c_pinky3.l",
        "c_ring1_base.l", "c_ring1.l", "c_ring2.l", "c_ring3.l",
        "c_middle1_base.l", "c_middle1.l", "c_middle2.l", "c_middle3.l",
        "c_index1_base.l", "c_index1.l", "c_index2.l", "c_index3.l",
        "c_thumb1_base.l", "c_thumb1.l", "c_thumb2.l", "c_thumb3.l"
    ]

    selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'ARMATURE']

    if selected_objects:
        armature = selected_objects[0]  
        bpy.ops.pose.select_all(action='DESELECT')
        
        for bone in armature.pose.bones:
            if bone.name in left_hand_bones:
                bone.bone.select = True

def seleccionar_huesos_right_hand():
    """Selecciona los huesos de la mano derecha en el armature seleccionado."""
    right_hand_bones = [
        "c_pinky1_base.r", "c_pinky1.r", "c_pinky2.r", "c_pinky3.r",
        "c_ring1_base.r", "c_ring1.r", "c_ring2.r", "c_ring3.r",
        "c_middle1_base.r", "c_middle1.r", "c_middle2.r", "c_middle3.r",
        "c_index1_base.r", "c_index1.r", "c_index2.r", "c_index3.r",
        "c_thumb1_base.r", "c_thumb1.r", "c_thumb2.r", "c_thumb3.r"
    ]

    selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'ARMATURE']

    if selected_objects:
        armature = selected_objects[0]  
        bpy.ops.pose.select_all(action='DESELECT')
        
        for bone in armature.pose.bones:
            if bone.name in right_hand_bones:
                bone.bone.select = True

def apply_phoneme_config(phoneme_name):
    print(f"Aplicando configuración para el fonema: {phoneme_name}")

    # Verificar si el fonema existe en el diccionario
    if phoneme_name not in phoneme_configs:
        print(f"Error: El fonema '{phoneme_name}' no está definido en las configuraciones.")
        return

    # Obtener la configuración del fonema
    config = phoneme_configs[phoneme_name]

    # Resetear las transformaciones de todos los objetos seleccionados
    for obj in bpy.context.selected_objects:
        obj.location = (0.0, 0.0, 0.0)  # Resetear la posición a (0, 0, 0)
        print(f"Transformaciones reseteadas para el objeto: {obj.name}")

    # Aplicar las nuevas coordenadas a los objetos con el mismo nombre
    for controller_name, (value_x, value_y) in config.items():
        controller_obj = bpy.data.objects.get(controller_name)
        if controller_obj and controller_obj in bpy.context.selected_objects:
            controller_obj.location.x = value_x
            controller_obj.location.y = value_y
            print(f"Coordenadas aplicadas a '{controller_name}': ({value_x}, {value_y})")
        else:
            print(f"Advertencia: El controlador '{controller_name}' no está seleccionado o no existe en la escena.")

    # Agregar un keyframe para todos los objetos seleccionados
    for obj in bpy.context.selected_objects:
        obj.keyframe_insert(data_path="location", index=-1)  # Insertar keyframe para la ubicación
        print(f"Keyframe añadido para el objeto: {obj.name}")

    print(f"Configuración del fonema '{phoneme_name}' aplicada correctamente.")

def Linker():
    print("Ejecutando Linker")
    selected_obj = bpy.context.object
    if not selected_obj or not selected_obj.data.shape_keys:
        print("Error: No hay un objeto seleccionado o no tiene Shape Keys.")
    else:
        shape_keys = selected_obj.data.shape_keys.key_blocks
        riggui_collection = bpy.data.collections.get("RIGGUI")
        if not riggui_collection:
            print("Error: La colección 'RIGGUI' no existe en la escena.")
        else:
            for shape_key_name, (controller_name, (axis, direction)) in control_pairs.items():
                shape_key = shape_keys.get(shape_key_name)
                controller_obj = riggui_collection.objects.get(controller_name)
                if shape_key and controller_obj:
                    axis_index = 0 if axis == "X" else 1
                    driver = shape_key.driver_add("value")
                    driver.driver.type = 'SCRIPTED'
                    var = driver.driver.variables.new()
                    var.name = "controller_pos"
                    var.type = 'TRANSFORMS'
                    target = var.targets[0]
                    target.id = controller_obj
                    target.transform_type = f"LOC_{axis}"
                    target.transform_space = 'LOCAL_SPACE'
                    if direction == -1:
                        driver.driver.expression = "max(0, min(1, -controller_pos))"
                    else:
                        driver.driver.expression = "max(0, min(1, controller_pos))"
                    print(f"Driver agregado: '{controller_name}' controla '{shape_key_name}' en eje {axis} ({'Negativo' if direction == -1 else 'Positivo'})")
                else:
                    print(f"Error: No se encontraron '{shape_key_name}' o '{controller_name}' en la colección 'RIGGUI'.")

def Unlink():
    print("Ejecutando Unlink")
    obj = bpy.context.active_object
    if obj and obj.data.shape_keys:
        shape_keys = obj.data.shape_keys.key_blocks
        anim_data = obj.data.shape_keys.animation_data
        if anim_data:
            for driver in anim_data.drivers:
                if driver.data_path.startswith("key_blocks["):
                    anim_data.drivers.remove(driver)
            print("Drivers eliminados de todos los shape keys.")
        else:
            print("No hay drivers asociados a los shape keys.")
    else:
        print("El objeto no tiene shape keys.")

def Clearshapes():
    print("Ejecutando Clearshapes")
    obj = bpy.context.active_object

    # Verificar si el objeto tiene shape keys
    if obj and obj.data.shape_keys:
        # Obtener los shape keys
        shape_keys = obj.data.shape_keys.key_blocks
        
        # Obtener la animación de datos (animation data) del objeto
        anim_data = obj.data.shape_keys.animation_data
        
        if anim_data:
            # Recorrer todos los shape keys
            for shape_key in shape_keys:
                # Establecer el valor del shape key a 0
                shape_key.value = 0
                
                # Obtener la ruta de datos (data path) del shape key
                data_path = f'key_blocks["{shape_key.name}"].value'
                
                # Buscar y eliminar los keyframes asociados al shape key
                if anim_data.action:
                    for fcurve in anim_data.action.fcurves:
                        if fcurve.data_path == data_path:
                            # Eliminar todos los keyframes del fcurve
                            anim_data.action.fcurves.remove(fcurve)
            
            print("Todos los valores de los shape keys han sido establecidos a 0 y los keyframes eliminados.")
        else:
            print("No hay animación asociada a los shape keys.")
    else:
        print("El objeto no tiene shape keys.")

def Bake_ctrlstoshapes():
    print("Ejecutando Bake_ctrlstoshapes")
    selected_obj = bpy.context.object
    if not selected_obj or not selected_obj.data.shape_keys:
        print("Error: No hay un objeto seleccionado o no tiene Shape Keys.")
    else:
        shape_keys = selected_obj.data.shape_keys
        riggui_collection = bpy.data.collections.get("RIGGUI")
        if not riggui_collection:
            print("Error: La colección 'RIGGUI' no existe en la escena.")
        else:
            shape_key_curves = {}
            for shape_key_name, (controller_name, (axis, direction)) in control_pairs.items():
                shape_key = shape_keys.key_blocks.get(shape_key_name)
                controller_obj = riggui_collection.objects.get(controller_name)
                if shape_key and controller_obj:
                    axis_index = 0 if axis == "X" else 1
                    if not controller_obj.animation_data or not controller_obj.animation_data.action:
                        print(f"Advertencia: El controlador '{controller_name}' no tiene datos de animación.")
                        continue
                    controller_action = controller_obj.animation_data.action
                    fcurve = next((fc for fc in controller_action.fcurves if fc.data_path == "location" and fc.array_index == axis_index), None)
                    if fcurve:
                        if not shape_keys.animation_data:
                            shape_keys.animation_data_create()
                        if not shape_keys.animation_data.action:
                            shape_keys.animation_data.action = bpy.data.actions.new(name=f"{selected_obj.name}_ShapeKey_Action")
                        shape_key_action = shape_keys.animation_data.action
                        shape_key_path = f'key_blocks["{shape_key.name}"].value'
                        if shape_key_name not in shape_key_curves:
                            shape_key_fcurve = shape_key_action.fcurves.find(shape_key_path)
                            if not shape_key_fcurve:
                                shape_key_fcurve = shape_key_action.fcurves.new(data_path=shape_key_path, index=0)
                            shape_key_fcurve.keyframe_points.clear()
                            shape_key_curves[shape_key_name] = shape_key_fcurve
                        else:
                            shape_key_fcurve = shape_key_curves[shape_key_name]
                        for kp in fcurve.keyframe_points:
                            frame, value = kp.co
                            new_value = value if direction > 0 else -value
                            existing_kp = next((p for p in shape_key_fcurve.keyframe_points if p.co.x == frame), None)
                            if existing_kp:
                                existing_kp.co.y += new_value
                            else:
                                shape_key_fcurve.keyframe_points.insert(frame, new_value)
                        print(f"Animación copiada de '{controller_name}' a Shape Key '{shape_key_name}' en el eje {axis} ({'Negativo' if direction == -1 else 'Positivo'})")
            print("Todas las animaciones han sido copiadas correctamente a los Shape Keys.")

def Bake_Shapestoctrls():
    print("Ejecutando Bake_Shapestoctrls")
    selected_obj = bpy.context.object
    if not selected_obj or not selected_obj.data.shape_keys:
        print("Error: No hay un objeto seleccionado o no tiene Shape Keys.")
    else:
        shape_keys = selected_obj.data.shape_keys
        if not shape_keys.animation_data or not shape_keys.animation_data.action:
            print("Error: No hay animaciones en los Shape Keys.")
        else:
            shape_key_action = shape_keys.animation_data.action
            riggui_collection = bpy.data.collections.get("RIGGUI")
            if not riggui_collection:
                print("Error: La colección 'RIGGUI' no existe en la escena.")
            else:
                controller_curves = {}
                for shape_key_name, (controller_name, (axis, direction)) in control_pairs.items():
                    shape_key = shape_keys.key_blocks.get(shape_key_name)
                    controller_obj = riggui_collection.objects.get(controller_name)
                    if shape_key and controller_obj:
                        fcurve = shape_key_action.fcurves.find(f'key_blocks["{shape_key.name}"].value')
                        if fcurve:
                            axis_index = 0 if axis == "X" else 1
                            if not controller_obj.animation_data:
                                controller_obj.animation_data_create()
                            if not controller_obj.animation_data.action:
                                controller_obj.animation_data.action = bpy.data.actions.new(name=f"{controller_name}_Action")
                            controller_action = controller_obj.animation_data.action
                            path = f'location[{axis_index}]'
                            if controller_name not in controller_curves:
                                controller_curves[controller_name] = {}
                            if path not in controller_curves[controller_name]:
                                ctrl_fcurve = controller_action.fcurves.find(path)
                                if not ctrl_fcurve:
                                    ctrl_fcurve = controller_action.fcurves.new(data_path="location", index=axis_index)
                                ctrl_fcurve.keyframe_points.clear()
                                controller_curves[controller_name][path] = ctrl_fcurve
                            else:
                                ctrl_fcurve = controller_curves[controller_name][path]
                            for kp in fcurve.keyframe_points:
                                frame, value = kp.co
                                new_value = max(-1, min(1, value if direction > 0 else -value))
                                existing_kp = next((p for p in ctrl_fcurve.keyframe_points if p.co.x == frame), None)
                                if existing_kp:
                                    # Se reemplaza el valor existente sin sumarlo
                                    existing_kp.co.y = new_value
                                else:
                                    ctrl_fcurve.keyframe_points.insert(frame, new_value)
                            print(f"Animación copiada de Shape Key '{shape_key_name}' a '{controller_name}' en el eje {axis} ({'Negativo' if direction == -1 else 'Positivo'})")
                print("Todas las animaciones han sido copiadas correctamente a los controladores.")
               
def Keyshapes():
    print("Ejecutando Keyshapes")
    selected_obj = bpy.context.object
    if selected_obj and selected_obj.type == 'MESH' and selected_obj.data.shape_keys:
        shape_keys = selected_obj.data.shape_keys.key_blocks
        current_frame = bpy.context.scene.frame_current
        for shape_key in shape_keys:
            shape_key.value = shape_key.value
            shape_key.keyframe_insert(data_path="value", frame=current_frame)
        print("Keyframed all shape keys.")
    else:
        print("No shape keys found on the active object.")

# Función para seleccionar objetos
def seleccionar_objetos(lista_objetos):
    bpy.ops.object.select_all(action='DESELECT')  # Deseleccionar todos los objetos
    for obj in bpy.data.objects:
        if obj.name in lista_objetos:
            obj.select_set(True)  # Seleccionar el objeto
            bpy.context.view_layer.objects.active = obj  # Asegurar que se mantenga activo

# operadores para cada fonema

class SeleccionarLeftHandBonesOperator(bpy.types.Operator):
    """Seleccionar huesos de la mano izquierda"""
    bl_idname = "object.seleccionar_left_hand_bones"
    bl_label = "Seleccionar Huesos Left Hand"

    def execute(self, context):
        seleccionar_huesos_left_hand()
        return {'FINISHED'}

class SeleccionarRightHandBonesOperator(bpy.types.Operator):
    """Seleccionar huesos de la mano right"""
    bl_idname = "object.seleccionar_right_hand_bones"
    bl_label = "Seleccionar Huesos Right Hand"

    def execute(self, context):
        seleccionar_huesos_right_hand()
        return {'FINISHED'}

class ApplyPhonemeFVOperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_fv"
    bl_label = "Aplicar FV"
    bl_description = "Aplica la configuración del fonema FV"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("FV")
        return {'FINISHED'}

class ApplyPhonemeAEOperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_ae"
    bl_label = "Aplicar AE"
    bl_description = "Aplica la configuración del fonema AE"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("AE")
        return {'FINISHED'}

class ApplyPhonemeAHOperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_ah"
    bl_label = "Aplicar AH"
    bl_description = "Aplica la configuración del fonema AH"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("AH")
        return {'FINISHED'}

class ApplyPhonemeBMPOperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_bmp"
    bl_label = "Aplicar BMP"
    bl_description = "Aplica la configuración del fonema BMP"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("BMP")
        return {'FINISHED'}

class ApplyPhonemeChJOperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_chj"
    bl_label = "Aplicar ChJ"
    bl_description = "Aplica la configuración del fonema ChJ"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("ChJ")
        return {'FINISHED'}
    
class ApplyPhonemeEESZTLDNOperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_eesztldn"
    bl_label = "Aplicar EESZTLDN"
    bl_description = "Aplica la configuración del fonema EESZTLDN"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("EESZTLDN")
        return {'FINISHED'}
    
class ApplyPhonemeErOperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_er"
    bl_label = "Aplicar Er"
    bl_description = "Aplica la configuración del fonema Er"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("Er")
        return {'FINISHED'}

class ApplyPhonemeIhOperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_ih"
    bl_label = "Aplicar Ih"
    bl_description = "Aplica la configuración del fonema Ih"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("Ih")
        return {'FINISHED'}

class ApplyPhonemeKGHNGOperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_kghng"
    bl_label = "Aplicar KGHNG"
    bl_description = "Aplica la configuración del fonema KGHNG"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("KGHNG")
        return {'FINISHED'}

class ApplyPhonemeOhOperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_oh"
    bl_label = "Aplicar Oh"
    bl_description = "Aplica la configuración del fonema Oh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("Oh")
        return {'FINISHED'}

class ApplyPhonemeROperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_r"
    bl_label = "Aplicar R"
    bl_description = "Aplica la configuración del fonema R"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("R")
        return {'FINISHED'}

class ApplyPhonemeThOperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_th"
    bl_label = "Aplicar Th"
    bl_description = "Aplica la configuración del fonema Th"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("Th")
        return {'FINISHED'}
    
class ApplyPhonemeWOOOperator(bpy.types.Operator):
    bl_idname = "object.apply_phoneme_woo"
    bl_label = "Aplicar WOO"
    bl_description = "Aplica la configuración del fonema WOO"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        apply_phoneme_config("WOO")
        return {'FINISHED'}

class MIADDON_OT_Linker(bpy.types.Operator):
    bl_idname = "miaddon.linker"
    bl_label = "Ejecutar Linker"

    def execute(self, context):
        Linker()
        return {'FINISHED'}

class MIADDON_OT_Unlink(bpy.types.Operator):
    bl_idname = "miaddon.unlink"
    bl_label = "Ejecutar Unlink"

    def execute(self, context):
        Unlink()
        return {'FINISHED'}

class MIADDON_OT_Clearshapes(bpy.types.Operator):
    bl_idname = "miaddon.clearshapes"
    bl_label = "Ejecutar Clearshapes"

    def execute(self, context):
        Clearshapes()
        return {'FINISHED'}
    
class MIADDON_OT_Bake_ctrlstoshapes(bpy.types.Operator):
    bl_idname = "miaddon.bake_ctrlstoshapes"
    bl_label = "Ejecutar Bake_ctrlstoshapes"

    def execute(self, context):
        Bake_ctrlstoshapes()
        return {'FINISHED'}

class MIADDON_OT_Bake_Shapestoctrls(bpy.types.Operator):
    bl_idname = "miaddon.bake_shapestoctrls"
    bl_label = "Ejecutar Bake_Shapestoctrls"

    def execute(self, context):
        Bake_Shapestoctrls()
        return {'FINISHED'}
    
class MIADDON_OT_Keyshapes(bpy.types.Operator):
    bl_idname = "miaddon.keyshapes"
    bl_label = "Ejecutar Keyshapes"

    def execute(self, context):
        Keyshapes()
        return {'FINISHED'}

class OBJECT_OT_select_riggui(bpy.types.Operator):
    """Selecciona todos los objetos dentro de la colección 'RIGGUI', excluyendo 'CTRL_faceGUI'"""
    bl_idname = "object.select_riggui"
    bl_label = "Select RIGGUI"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Nombre de la colección a seleccionar
        collection_name = "RIGGUI"

        # Obtener la colección
        riggui_collection = bpy.data.collections.get(collection_name)

        if not riggui_collection:
            self.report({'ERROR'}, f"La colección '{collection_name}' no existe en la escena.")
            return {'CANCELLED'}

        # Deseleccionar todo antes de seleccionar los objetos en la colección
        bpy.ops.object.select_all(action='DESELECT')

        # Seleccionar todos los objetos dentro de la colección, excluyendo 'CTRL_faceGUI'
        for obj in riggui_collection.objects:
            if obj.name != "CTRL_faceGUI":  # Excluir este objeto específico
                obj.select_set(True)

        self.report({'INFO'}, f"Todos los objetos en la colección '{collection_name}', excepto 'CTRL_faceGUI', han sido seleccionados.")
        return {'FINISHED'}

class SeleccionarObjetosBrowsOperator(bpy.types.Operator):
    bl_idname = "object.seleccionar_objetos_brows"
    bl_label = "Sel Brows"
    bl_description = "Selecciona los objetos relacionados con las cejas en el viewport"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        seleccionar_objetos(objetos_brows)  # Pasar la lista correspondiente
        return {'FINISHED'}

class SeleccionarObjetosMidHeadOperator(bpy.types.Operator):
    bl_idname = "object.seleccionar_objetos_mid_head"
    bl_label = "Sel E-N-E"
    bl_description = "Selecciona los objetos relacionados con ojos, nariz y orejas"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        seleccionar_objetos(objetos_mid_Head)  # Pasar la lista correspondiente
        return {'FINISHED'}

class SeleccionarObjetosMouthJawOperator(bpy.types.Operator):
    bl_idname = "object.seleccionar_objetos_mouth_jaw"
    bl_label = "Sel Mouth-Jaw"
    bl_description = "Selecciona los objetos relacionados con la boca y la mandíbula"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        seleccionar_objetos(objetos_mouth_jaw)  # Pasar la lista correspondiente
        return {'FINISHED'}

# Class para Blenshapes

class MIADDON_PT_Panel(bpy.types.Panel):
    bl_label = "CTRLsAndShapes Panel"
    bl_idname = "MIADDON_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'GothaLinkerV2'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text='Linking head and shapes', icon='OUTLINER')

        row = layout.row()
        row.operator("miaddon.linker", text="Linker", icon='LINKED')
        row.operator("miaddon.unlink", text="Unlink", icon='UNLINKED')

        row = layout.row()
        row.label(text='Key&Clear', icon='MONKEY')
        row = layout.row()        
        row.operator("miaddon.clearshapes", text="Clearshapes", icon='MATFLUID')
        row.operator("miaddon.keyshapes", text="Keyshapes", icon='KEYINGSET')

        row = layout.row()
        row.label(text='Bake Ctrls&Shapes', icon='RESTRICT_SELECT_OFF')

        row = layout.row()
        row.operator("miaddon.bake_ctrlstoshapes", text="Bake_ctrlstoshapes")

        row = layout.row()
        row.operator("miaddon.bake_shapestoctrls", text="Bake_Shapestoctrls")

        row = layout.row()
        row.label(text='SET SELECTORS', icon='RESTRICT_SELECT_OFF')

        row = layout.row()       
        row.operator("object.select_riggui", text="Select RIGGUI")
        
        row = layout.row()
        row.operator("object.seleccionar_objetos_brows", text="Sel Brows")
        row.operator("object.seleccionar_objetos_mid_head", text="Sel E-N-E")
        row.operator("object.seleccionar_objetos_mouth_jaw", text="Sel Mouth-Jaw")
        row = layout.row()
        row.operator("object.seleccionar_left_hand_bones", text="L_Fingers")
        row.operator("object.seleccionar_right_hand_bones", text="R_Fingers")

        # Botones para los fonemas
        row = layout.row()
        row.label(text='SET PHONEMES', icon='STATUSBAR')
        row = layout.row()
        row.operator("object.apply_phoneme_fv", text="FV")
        row.operator("object.apply_phoneme_ae", text="AE")
        row.operator("object.apply_phoneme_ah", text="AH")
        row.operator("object.apply_phoneme_bmp", text="BMP")

        row = layout.row()
        row.operator("object.apply_phoneme_chj", text="ChJ")
        row.operator("object.apply_phoneme_eesztldn", text="EESZTLDN")
        row.operator("object.apply_phoneme_er", text="Er")
        row.operator("object.apply_phoneme_ih", text="Ih")
        
        row = layout.row()
        row.operator("object.apply_phoneme_kghng", text="KGHNG")
        row.operator("object.apply_phoneme_oh", text="Oh")
        row.operator("object.apply_phoneme_r", text="R")
        row.operator("object.apply_phoneme_th", text="Th")

        row = layout.row()
        row.operator("object.apply_phoneme_woo", text="WOO")

        row = layout.row()
        row.label(text="Aligner Tool", icon='GROUP_VCOL')
        row = layout.row()
        row.prop(context.scene, "Target")  # Input para seleccionar el Target
        row.prop(context.scene, "Object")  # Input para seleccionar el Object
        row.operator("Copy Loc-Rot")  # Botón para copiar transformaciones

def register():
    try:
        bpy.utils.register_class(MIADDON_PT_Panel)
    except ValueError:
        print("MIADDON_PT_Panel ya está registrado.")
    
    # Registrar otras clases
    bpy.utils.register_class(MIADDON_OT_Linker)
    bpy.utils.register_class(MIADDON_OT_Unlink)
    bpy.utils.register_class(MIADDON_OT_Clearshapes)
    bpy.utils.register_class(MIADDON_OT_Bake_ctrlstoshapes)
    bpy.utils.register_class(MIADDON_OT_Bake_Shapestoctrls)
    bpy.utils.register_class(MIADDON_OT_Keyshapes)
    bpy.utils.register_class(OBJECT_OT_select_riggui)
    bpy.utils.register_class(SeleccionarObjetosBrowsOperator)
    bpy.utils.register_class(SeleccionarObjetosMidHeadOperator)
    bpy.utils.register_class(SeleccionarObjetosMouthJawOperator)
    bpy.utils.register_class(ApplyPhonemeFVOperator)
    bpy.utils.register_class(ApplyPhonemeAEOperator)
    bpy.utils.register_class(ApplyPhonemeAHOperator)
    bpy.utils.register_class(ApplyPhonemeBMPOperator)
    bpy.utils.register_class(ApplyPhonemeChJOperator)
    bpy.utils.register_class(ApplyPhonemeEESZTLDNOperator)
    bpy.utils.register_class(ApplyPhonemeErOperator)
    bpy.utils.register_class(ApplyPhonemeIhOperator)
    bpy.utils.register_class(ApplyPhonemeKGHNGOperator)
    bpy.utils.register_class(ApplyPhonemeOhOperator)
    bpy.utils.register_class(ApplyPhonemeROperator)
    bpy.utils.register_class(ApplyPhonemeThOperator)
    bpy.utils.register_class(ApplyPhonemeWOOOperator)
    bpy.utils.register_class(SeleccionarLeftHandBonesOperator)
    bpy.utils.register_class(SeleccionarRightHandBonesOperator)
    
def unregister():
    bpy.utils.unregister_class(MIADDON_PT_Panel)
    bpy.utils.unregister_class(MIADDON_OT_Linker)
    bpy.utils.unregister_class(MIADDON_OT_Unlink)
    bpy.utils.unregister_class(MIADDON_OT_Clearshapes)
    bpy.utils.unregister_class(MIADDON_OT_Bake_ctrlstoshapes)
    bpy.utils.unregister_class(MIADDON_OT_Bake_Shapestoctrls)
    bpy.utils.unregister_class(MIADDON_OT_Keyshapes)
    bpy.utils.unregister_class(OBJECT_OT_select_riggui)
    bpy.utils.unregister_class(SeleccionarObjetosBrowsOperator)
    bpy.utils.unregister_class(SeleccionarObjetosMidHeadOperator)
    bpy.utils.unregister_class(SeleccionarObjetosMouthJawOperator)
    bpy.utils.unregister_class(ApplyPhonemeFVOperator)
    bpy.utils.unregister_class(ApplyPhonemeAEOperator)
    bpy.utils.unregister_class(ApplyPhonemeAHOperator)
    bpy.utils.unregister_class(ApplyPhonemeBMPOperator)
    bpy.utils.unregister_class(ApplyPhonemeChJOperator)
    bpy.utils.unregister_class(ApplyPhonemeEESZTLDNOperator)
    bpy.utils.unregister_class(ApplyPhonemeErOperator)
    bpy.utils.unregister_class(ApplyPhonemeIhOperator)
    bpy.utils.unregister_class(ApplyPhonemeKGHNGOperator)
    bpy.utils.unregister_class(ApplyPhonemeOhOperator)
    bpy.utils.unregister_class(ApplyPhonemeROperator)
    bpy.utils.unregister_class(ApplyPhonemeThOperator)
    bpy.utils.unregister_class(ApplyPhonemeWOOOperator)
    bpy.utils.unregister_class(SeleccionarLeftHandBonesOperator)
    bpy.utils.unregister_class(SeleccionarRightHandBonesOperator)
    

    
if __name__ == "__main__":
    register()