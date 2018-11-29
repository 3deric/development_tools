import bpy
from math import *

def rotateLeft(length, value):
    mask = 2**length - 1
    carry_pos = 2**(length - 1)
    return ((value << 1) | int(bool(value & carry_pos))) & mask

for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        bpy.context.scene.objects.active = obj
        
        prefix = ''
        name = str(obj.name)
        
        if '_' in name:
            prefix, name = name.split('_')
            prefix = prefix + '_' 
                
        binary = format(int(name) ,'08b')
            
        p0 = int(binary[:4],2)
        p1 = int(binary[4:],2)
        
        for i in range(1, 4):
            p0 = rotateLeft(4, p0)
            p1 = rotateLeft(4, p1)
            
            result = prefix + str(int(str(format(p0, '04b')) + str(format(p1, '04b')),2))
            
            if bpy.data.objects.get(result) is None:
                new_obj = obj.copy()
                new_obj.data = obj.data.copy()
                bpy.context.scene.objects.link(new_obj)
                bpy.context.scene.objects.active = new_obj
                bpy.context.scene.objects.active.name = result
                bpy.context.active_object.rotation_euler = (0, 0, pi/2 * i)
                bpy.context.active_object.location = (0, 0, 0)
                bpy.ops.object.transform_apply(location = True, scale = True, rotation = True)  
