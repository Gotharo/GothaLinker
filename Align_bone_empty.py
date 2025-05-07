import bpy

def update_list(self, context):
    """Filtrar objetos Empty y bones con 'ik' en su nombre"""
    filtered_objects = [(obj.name, obj.name, "") for obj in bpy.data.objects if obj.type == 'EMPTY']
    
    armature_obj = bpy.context.object
    if armature_obj and armature_obj.type == 'ARMATURE':
        filtered_bones = [(bone.name, bone.name, "") for bone in armature_obj.pose.bones if "ik" in bone.name.lower()]
        filtered_objects.extend(filtered_bones)

    return filtered_objects

class CopyTransformsOperator(bpy.types.Operator):
    """Operador para aplicar la transformación"""
    bl_idname = "object.copy_transforms"
    bl_label = "Copiar Transformaciones"

    def execute(self, context):
        target_name = context.scene.target_dropdown
        object_name = context.scene.object_dropdown

        target_obj = bpy.data.objects.get(target_name)  # Buscar si Target es un objeto
        object_obj = bpy.data.objects.get(object_name)  # Buscar si Object es un objeto

        armature_obj = bpy.context.object  # Armature seleccionado

        # Si el Target no es un objeto, buscarlo como bone dentro del Armature activo
        if not target_obj and armature_obj and armature_obj.type == 'ARMATURE':
            target_bone = armature_obj.pose.bones.get(target_name)
        else:
            target_bone = None

        # Si el Object no es un objeto, buscarlo como bone dentro del Armature activo
        if not object_obj and armature_obj and armature_obj.type == 'ARMATURE':
            object_bone = armature_obj.pose.bones.get(object_name)
        else:
            object_bone = None

        # Validaciones de existencia
        if not (target_obj or target_bone):
            self.report({'ERROR'}, f"El Target '{target_name}' no se encontró en la escena ni en el Armature activo.")
            return {'CANCELLED'}
        if not (object_obj or object_bone):
            self.report({'ERROR'}, f"El Object '{object_name}' no se encontró en la escena ni en el Armature activo.")
            return {'CANCELLED'}

        # Obtener la matriz mundial del Target
        if target_obj:
            world_matrix = target_obj.matrix_world
        elif target_bone:
            world_matrix = armature_obj.matrix_world @ target_bone.matrix

        # Calcular la distancia real entre el Empty y el hueso
        if target_obj and object_bone:
            target_location = target_obj.matrix_world.translation
            bone_world_location = (armature_obj.matrix_world @ object_bone.matrix).translation
            offset_vector = target_location - bone_world_location

            # Ajustar la posición del hueso en Pose Space
            object_bone.location = armature_obj.matrix_world.inverted() @ offset_vector

        # Copiar la rotación del Empty al hueso
        if target_obj and object_bone:
            target_rotation = target_obj.matrix_world.to_quaternion()
            object_bone.rotation_quaternion = target_rotation @ armature_obj.matrix_world.to_quaternion().inverted()

        # Aplicar la transformación al Object (puede ser un objeto o un bone)
        if object_obj:
            object_obj.matrix_world = world_matrix  # Copia directa si es un objeto
            object_obj.keyframe_insert(data_path="location")  # Agregar keyframe para la ubicación
            object_obj.keyframe_insert(data_path="rotation_euler")  # Agregar keyframe para la rotación
        elif object_bone:
            # Agregar keyframes para el hueso
            object_bone.keyframe_insert(data_path="location")  # Agregar keyframe para la ubicación
            object_bone.keyframe_insert(data_path="rotation_quaternion")  # Agregar keyframe para la rotación

        # Agregar keyframes al Target si es un objeto
        if target_obj:
            target_obj.keyframe_insert(data_path="location")  # Agregar keyframe para la ubicación
            target_obj.keyframe_insert(data_path="rotation_euler")  # Agregar keyframe para la rotación

        self.report({'INFO'}, f"El Object '{object_name}' ahora copia la posición y rotación de '{target_name}' en World Space. Keyframes añadidos.")
        return {'FINISHED'}



# Funciones de registro y desregistro
def register():
    bpy.utils.register_class(CopyTransformsOperator)

def unregister():
    bpy.utils.unregister_class(CopyTransformsOperator)
