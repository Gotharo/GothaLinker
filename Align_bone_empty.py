import bpy

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

        # Convertir la matriz de World Space a Pose Space
        pose_matrix = armature_obj.matrix_world.inverted() @ world_matrix

        # Aplicar la transformación al Object (puede ser un objeto o un bone)
        if object_obj:
            object_obj.matrix_world = world_matrix  # Copia directa si es un objeto
            object_obj.keyframe_insert(data_path="location")  # Agregar keyframe para la ubicación
            object_obj.keyframe_insert(data_path="rotation_euler")  # Agregar keyframe para la rotación
        elif object_bone:
            object_bone.matrix = pose_matrix  # Copia la transformación si es un bone
            object_bone.keyframe_insert(data_path="location")  # Agregar keyframe para la ubicación
            object_bone.keyframe_insert(data_path="rotation_euler")  # Agregar keyframe para la rotación

        # Agregar keyframes al Target si es un objeto
        if target_obj:
            target_obj.keyframe_insert(data_path="location")  # Agregar keyframe para la ubicación
            target_obj.keyframe_insert(data_path="rotation_euler")  # Agregar keyframe para la rotación

        self.report({'INFO'}, f"El Object '{object_name}' ahora copia la posición y rotación de '{target_name}' en World Space. Keyframes añadidos.")
        return {'FINISHED'}

class LinkCopyTransformsOperator(bpy.types.Operator):
    """Aplica un modificador Copy Transforms y establece keyframes"""
    bl_idname = "object.link_copy_transforms"
    bl_label = "Link Copy Transforms"

    def execute(self, context):
        target_name = context.scene.target_dropdown
        object_name = context.scene.object_dropdown

        target_obj = bpy.data.objects.get(target_name)
        object_obj = bpy.data.objects.get(object_name)

        if not target_obj or not object_obj:
            self.report({'ERROR'}, "Target u Object no válidos.")
            return {'CANCELLED'}

        # Crear el modificador Copy Transforms
        modifier = object_obj.modifiers.new(name="Copy Transforms", type='COPY_TRANSFORMS')
        modifier.target = target_obj

        # Establecer keyframes para la influencia
        current_frame = bpy.context.scene.frame_current
        modifier.influence = 1.0
        modifier.keyframe_insert(data_path="influence", frame=current_frame)
        modifier.influence = 0.0
        modifier.keyframe_insert(data_path="influence", frame=current_frame - 1)

        self.report({'INFO'}, f"Modificador Copy Transforms aplicado de {target_name} a {object_name}.")
        return {'FINISHED'}

class UnlinkCopyTransformsOperator(bpy.types.Operator):
    """Desactiva el modificador Copy Transforms y establece keyframes"""
    bl_idname = "object.unlink_copy_transforms"
    bl_label = "Unlink Copy Transforms"

    def execute(self, context):
        object_name = context.scene.object_dropdown
        object_obj = bpy.data.objects.get(object_name)

        if not object_obj:
            self.report({'ERROR'}, "Object no válido.")
            return {'CANCELLED'}

        # Buscar el modificador Copy Transforms
        modifier = next((mod for mod in object_obj.modifiers if mod.type == 'COPY_TRANSFORMS'), None)
        if not modifier:
            self.report({'ERROR'}, "No se encontró un modificador Copy Transforms.")
            return {'CANCELLED'}

        # Establecer keyframes para la influencia
        current_frame = bpy.context.scene.frame_current
        modifier.influence = 1.0
        modifier.keyframe_insert(data_path="influence", frame=current_frame)
        modifier.influence = 0.0
        modifier.keyframe_insert(data_path="influence", frame=current_frame + 1)

        # Eliminar el modificador
        object_obj.modifiers.remove(modifier)

        self.report({'INFO'}, f"Modificador Copy Transforms eliminado de {object_name}.")
        return {'FINISHED'}

def update_list(self, context):
    """Filtrar objetos Empty y bones con 'ik' en su nombre"""
    filtered_objects = [(obj.name, obj.name, "") for obj in bpy.data.objects if obj.type == 'EMPTY']
    
    armature_obj = bpy.context.object
    if armature_obj and armature_obj.type == 'ARMATURE':
        filtered_bones = [(bone.name, bone.name, "") for bone in armature_obj.pose.bones if "ik" in bone.name.lower()]
        filtered_objects.extend(filtered_bones)

    return filtered_objects



# Funciones de registro y desregistro
def register():
    bpy.utils.register_class(CopyTransformsOperator)
    bpy.utils.register_class(LinkCopyTransformsOperator)
    bpy.utils.register_class(UnlinkCopyTransformsOperator)

def unregister():
    bpy.utils.unregister_class(CopyTransformsOperator)
    bpy.utils.unregister_class(LinkCopyTransformsOperator)
    bpy.utils.unregister_class(UnlinkCopyTransformsOperator)
