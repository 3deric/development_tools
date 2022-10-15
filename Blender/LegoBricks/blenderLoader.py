import bpy, csv, numpy

fp = "/home/eric/IMG_4193.csv"

vertices = []
edges = []
faces = []

blocks = []
colours = []

with open( fp ) as csvfile:
    rdr = csv.reader( csvfile )
    for i, row in enumerate( rdr ):
        vertices.append((float(row[0]),float(row[1]),0))
        blocks.append(int(row[2]))
        colours.append(float(row[3])/256)
        colours.append(float(row[4])/256)
        colours.append(float(row[5])/256)

new_mesh = bpy.data.meshes.new('new_mesh')
new_mesh.from_pydata(vertices, edges, faces)
new_mesh.update()

new_mesh.attributes.new(name="blocks", type="INT", domain="POINT")
new_mesh.attributes["blocks"].data.foreach_set("value", blocks)

new_mesh.attributes.new(name='colours', type='FLOAT_VECTOR', domain='POINT')
#colours = numpy.zeros(len(new_mesh.vertices) * 3, dtype=numpy.float32)
new_mesh.attributes['colours'].data.foreach_set('vector', colours)

new_object = bpy.data.objects.new('new_object', new_mesh)

new_collection = bpy.data.collections.new('new_collection')
bpy.context.scene.collection.children.link(new_collection)

new_collection.objects.link(new_object)
