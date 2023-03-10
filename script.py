import bpy
import random
import json
import time


def clean_scene():
    if bpy.context.active_object and bpy.context.active_object.mode == "EDIT":
        bpy.ops.object.editmode_toggle()
    for obj in bpy.data.objects:
        obj.hide_set(False)
        obj.hide_select = False
        obj.hide_viewport = False
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    collection_names = [col.name for col in bpy.data.collections]
    for name in collection_names:
        bpy.data.collections.remove(bpy.data.collections[name])
    world_names = [world.name for world in bpy.data.worlds]
    for name in world_names:
        bpy.data.worlds.remove(bpy.data.worlds[name])
    bpy.ops.world.new()
    bpy.context.scene.world = bpy.data.worlds["World"]
    bpy.ops.outliner.orphans_purge(
        do_local_ids=True, do_linked_ids=True, do_recursive=True
    )
    for i in range(30):
        print()
    bpy.ops.object.select_all(action="DESELECT")


def parse_input_data(path):
    emotions_json = open(path + "emotions.json")
    state_emotions_dict_tree = json.load(emotions_json)
    state_emotions_dict = state_emotions_dict_tree["emotions"]
    state, parent_emotions_dict = random.choice(list(state_emotions_dict.items()))
    parent_emotion, emotion_dict = random.choice(list(parent_emotions_dict.items()))
    emotion, words = random.choice(list(emotion_dict.items()))
    word = random.choice(words)
    emotions_json.close()
    location_json = open(path + "locations.json")
    locations = json.load(location_json)
    location, elements = random.choice(list(locations.items()))
    location_json.close()
    color_json = open(path + "colors.json")
    colors_dict = json.load(color_json)
    color_temperatures = {
        "positive": "warm",
        "negative": "cold",
        "neutral": random.choice(["warm", "cold"]),
    }
    color_temp = color_temperatures[state]
    color_name, shades = random.choice(list(colors_dict["colors"][color_temp].items()))
    shade = random.randrange(len(shades))
    color_hex = shades[shade]
    (r, g, b) = map(lambda x: x / 255, bytes.fromhex(color_hex[-6:]))
    color_json.close()
    translation_json = open(path + "translation.json")
    translations_dict_tree = json.load(translation_json)
    translations_dict = translations_dict_tree["translation"]
    translation_parameter = translations_dict[emotion]
    translation_json.close()
    if emotion == "neutral":
        for key, value in translation_parameter.items():
            translations_dict["neutral"][key] = random.choice(value)
        translation_parameter = translations_dict[emotion]
    return_dict = {
        "word": word,
        "emotion": emotion,
        "parent emotion": parent_emotion,
        "emotion state": state,
        "location": location,
        "elements": elements,
        "color_hex": color_hex,
        "color_rgb": (r, g, b),
        "colors": shades,
        "shade": shade,
        "color name": color_name,
        "color temperature": color_temp,
        "translation parameter": translation_parameter,
    }
    for key, value in return_dict.items():
        if key is not "translation parameter":
            print(key + ":", value)
    for key, value in translation_parameter.items():
        print(key + ":", value)
    return return_dict


def import_modules(modules, path):
    for element in modules:
        file_name = element + ".obj"
        bpy.ops.wm.obj_import(
            filepath=path + "modules/arc.obj",
            directory=path + "modules/",
            files=[{"name": file_name}],
            forward_axis="Y",
            up_axis="Z",
        )
    bpy.ops.object.select_all(action="DESELECT")


def add_modifier_modules(path, amount_level):
    if "arc_0" in bpy.data.objects:
        amount = amount_level * amount_level
        arc_names = [0, 1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6]
        to_delete = arc_names[amount:]
        to_keep = arc_names[:amount]
        for arc in to_delete:
            arc_name = "arc_" + str(arc)
            bpy.data.objects.remove(bpy.data.objects[arc_name], do_unlink=True)
        bpy.context.view_layer.objects.active = bpy.data.objects["arc_0"]
        bpy.ops.object.select_pattern(pattern="arc*")
        bpy.ops.object.join()
        bpy.ops.object.select_all(action="DESELECT")
    if "corner_house" in bpy.data.objects:
        amount = 5 + amount_level
        corner_house = bpy.data.objects["corner_house"]
        mod = corner_house.modifiers.new("Array", "ARRAY")
        mod.relative_offset_displace = (0, 0, -1)
        mod.count = amount
        bpy.ops.object.select_all(action="DESELECT")
    if "dish" in bpy.data.objects:
        amount = 5
        for i in range(amount):
            bpy.ops.wm.obj_import(
                filepath=path + "modules/dish.obj",
                directory=path + "modules/",
                files=[{"name": "dish.obj"}],
                forward_axis="Y",
                up_axis="Z",
            )
            for obj in bpy.context.selected_objects:
                obj.name = "dish_" + str(i)
                obj.data.name = "dish_" + str(i)
        bpy.ops.object.select_all(action="DESELECT")
    if "fence" in bpy.data.objects:
        amount = 3 + amount_level
        fence = bpy.data.objects["fence"]
        mod = fence.modifiers.new("Array", "ARRAY")
        mod.relative_offset_displace = (1, 0, 0)
        mod.count = amount
        bpy.ops.object.select_all(action="DESELECT")
    if "apple" in bpy.data.objects:
        amount = amount_level
        for i in range(amount):
            bpy.ops.wm.obj_import(
                filepath=path + "modules/fruits.obj",
                directory=path + "modules/",
                files=[{"name": "fruits.obj"}],
                forward_axis="Y",
                up_axis="Z",
            )
        bpy.ops.object.select_all(action="DESELECT")
    if "horn_house" in bpy.data.objects:
        amount = 5 + amount_level
        horn_house = bpy.data.objects["horn_house"]
        mod = horn_house.modifiers.new("Array", "ARRAY")
        mod.relative_offset_displace = (0, 0, -1)
        mod.count = amount
        bpy.context.view_layer.objects.active = bpy.data.objects["horn_house"]
        bpy.ops.object.modifier_apply(modifier=mod.name)
        bpy.ops.object.select_pattern(pattern="horn_house*")
        bpy.ops.object.join()
        bpy.ops.object.select_all(action="DESELECT")
    if "skeleton_house" in bpy.data.objects:
        amount = 6 + amount_level
        skeleton_house = bpy.data.objects["skeleton_house"]
        mod = skeleton_house.modifiers.new("Array", "ARRAY")
        mod.relative_offset_displace = (0, 0, -1)
        mod.count = amount
        bpy.context.view_layer.objects.active = bpy.data.objects["skeleton_house"]
        bpy.ops.object.modifier_apply(modifier=mod.name)
        bpy.ops.object.select_pattern(pattern="skeleton_house*")
        bpy.ops.object.join()
        bpy.ops.object.select_all(action="DESELECT")
    if "subway_bridge" in bpy.data.objects:
        amount = 2 + amount_level
        subway_bridge = bpy.data.objects["subway_bridge"]
        mod = subway_bridge.modifiers.new("Array", "ARRAY")
        mod.relative_offset_displace = (1, 0, 0)
        mod.count = amount
        bpy.ops.object.select_all(action="DESELECT")
    if "metro_entrance" in bpy.data.objects:
        amount = amount_level
        for i in range(amount):
            bpy.ops.wm.obj_import(
                filepath=path + "modules/subway_entrance.obj",
                directory=path + "modules/",
                files=[{"name": "subway_entrance.obj"}],
                forward_axis="Y",
                up_axis="Z",
            )
        bpy.ops.object.select_all(action="DESELECT")
    if "subway_wall" in bpy.data.objects:
        amount = 2
        subway_wall = bpy.data.objects["subway_wall"]
        mod = subway_wall.modifiers.new("ArrayX", "ARRAY")
        mod.relative_offset_displace = (1, 0, 0)
        mod.count = amount
        mod = subway_wall.modifiers.new("Array-X", "ARRAY")
        mod.relative_offset_displace = (-1, 0, 0)
        mod.count = amount
        mod = subway_wall.modifiers.new("ArrayZ", "ARRAY")
        mod.relative_offset_displace = (0, 0, 1)
        mod.count = amount
        mod = subway_wall.modifiers.new("Array-Z", "ARRAY")
        mod.relative_offset_displace = (0, 0, -1)
        mod.count = amount
        bpy.ops.object.select_all(action="DESELECT")
    if "window" in bpy.data.objects:
        amount = 6 + amount_level * amount_level
        window = bpy.data.objects["window"]
        mod = window.modifiers.new("Array", "ARRAY")
        mod.relative_offset_displace = (1, 0, 0)
        mod.count = amount
        bpy.ops.object.select_all(action="DESELECT")


def import_word(word):
    font_curve = bpy.data.curves.new(type="FONT", name="word")
    font_curve.body = word
    obj = bpy.data.objects.new(name="word", object_data=font_curve)
    obj.data.align_x = "CENTER"
    obj.data.align_y = "CENTER"
    obj.location = (0, -15, 0)
    obj.rotation_euler[0] = 3.14159 * 90 / 180
    obj.data.extrude = 0.1
    obj.data.bevel_mode = "ROUND"
    obj.data.bevel_depth = 0.03
    bpy.context.scene.collection.objects.link(obj)
    bpy.data.objects["word"].select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.convert(target="MESH")
    bpy.ops.object.modifier_add(type="DECIMATE")
    bpy.context.object.modifiers["Decimate"].decimate_type = "DISSOLVE"
    bpy.ops.object.modifier_apply(modifier="Decimate")
    bpy.ops.object.select_all(action="DESELECT")


def setup_scene(color):
    bpy.ops.object.camera_add(location=(0, -35, 0), rotation=(1.5708, 0, 0))
    bpy.context.scene.camera = bpy.context.object
    bpy.context.scene.render.resolution_x = 7016
    bpy.context.scene.render.resolution_y = 9933
    bpy.context.scene.render.resolution_percentage = 30
    bpy.context.scene.render.film_transparent = False
    bpy.context.scene.world.color = color
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[
        0
    ].default_value = color + (1,)
    bpy.context.scene.render.engine = "CYCLES"
    bpy.context.scene.cycles.preview_samples = 8
    bpy.context.scene.cycles.samples = 8
    bpy.context.scene.cycles.use_denoising = False
    bpy.context.scene.cycles.use_fast_gi = True
    bpy.context.scene.view_settings.view_transform = "Standard"
    bpy.context.scene.render.use_freestyle = True
    bpy.context.scene.view_layers["ViewLayer"].use_freestyle = True
    bpy.context.scene.render.line_thickness_mode = "RELATIVE"
    if not bpy.data.linestyles:
        bpy.ops.scene.freestyle_lineset_add()
    bpy.data.linestyles["LineStyle"].alpha = 0.5
    bpy.data.linestyles["LineStyle"].thickness = 0.3
    bpy.data.linestyles["LineStyle"].color = (0, 0, 0)
    bpy.data.linestyles["LineStyle"].chaining = "SKETCHY"
    bpy.data.linestyles["LineStyle"].rounds = 8
    bpy.context.scene.view_layers["ViewLayer"].freestyle_settings.crease_angle = 2.44346
    bpy.context.scene.view_layers["ViewLayer"].freestyle_settings.linesets[
        "LineSet"
    ].select_crease = False
    bpy.context.scene.view_layers["ViewLayer"].freestyle_settings.use_culling = True
    mat_color = bpy.data.materials.new(name="material_color")
    mat_neutral = bpy.data.materials.new(name="material_neutral")
    mat_color.diffuse_color = color + (1,)
    mat_neutral.diffuse_color = (1, 1, 1, 1)
    bpy.ops.object.select_all(action="DESELECT")


def random_apply_materials():
    mat_color = bpy.data.materials.get("material_color")
    mat_neutral = bpy.data.materials.get("material_neutral")
    for obj in bpy.context.scene.objects:
        obj.select_set(obj.type == "MESH" or obj.type == "FONT")
    if random.randint(0, 1):
        for o in bpy.context.selected_objects:
            o.data.materials.append(mat_color)
        if random.randint(0, 1):
            bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[
                0
            ].default_value = (1, 1, 1, 1)
    else:
        for o in bpy.context.selected_objects:
            o.data.materials.append(mat_neutral)
    bpy.ops.object.select_all(action="DESELECT")


def render(path, emotion, seed):
    bpy.context.scene.render.resolution_percentage = 30
    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.render.filepath = (
        path + "out/" + emotion + "_" + str(seed) + ".png"
    )
    bpy.ops.render.render(write_still=True)
    return True


def set_seed(defined_seed):
    if not defined_seed:
        seed = int(time.time() * 10000000)
    else:
        seed = defined_seed
    random.seed(seed)
    print("seed:", seed)
    return seed


def sharpness_translator(value):
    if value == "blurry":
        bpy.data.cameras["Camera"].dof.use_dof = True
        bpy.data.cameras["Camera"].dof.focus_distance = 4
        bpy.ops.scene.freestyle_thickness_modifier_add(type="DISTANCE_FROM_CAMERA")
        bpy.data.linestyles["LineStyle"].thickness_modifiers[
            "Distance from Camera"
        ].invert = True
    elif value == "sharp":
        bpy.data.cameras["Camera"].dof.use_dof = False
        mod_list = bpy.data.linestyles["LineStyle"].thickness_modifiers
        for mod in mod_list:
            bpy.data.linestyles["LineStyle"].thickness_modifiers.remove(mod)
    else:
        raise Exception("something went wrong")
    bpy.ops.object.select_all(action="DESELECT")


def shade_translator(value, input_dict):
    if value == "light":
        colors = input_dict["colors"][:2]
    elif value == "medium":
        colors = input_dict["colors"][2:-2]
    elif value == "dark":
        colors = input_dict["colors"][-2:]
    else:
        raise Exception("something went wrong")
    color_hex = random.choice(colors)
    (r, g, b) = map(lambda x: x / 255, bytes.fromhex(color_hex[-6:]))
    mat_color = bpy.data.materials["material_color"]
    mat_color.diffuse_color = (r, g, b) + (1,)
    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (
        r,
        g,
        b,
    ) + (1,)
    bpy.ops.object.select_all(action="DESELECT")


def element_amount_translator(value, path):
    if value == "single":
        add_modifier_modules(path, 0)
        bpy.ops.object.select_by_type(type="MESH")
        selection = bpy.context.selected_objects
        random.shuffle(selection)
        for i in range(len(selection) - 1):
            element = selection[i]
            bpy.data.objects.remove(bpy.data.objects[element.name], do_unlink=True)
    elif value == "few":
        add_modifier_modules(path, 1)
    elif value == "medium":
        add_modifier_modules(path, 2)
    elif value == "many":
        add_modifier_modules(path, 3)
    elif value == "full":
        add_modifier_modules(path, 4)
    else:
        raise Exception("something went wrong")
    bpy.ops.object.select_all(action="DESELECT")


def element_concentration_translator(value):
    if value == "far":
        loc_range = (7, 7, 10)
    elif value == "medium":
        loc_range = (5, 5, 8)
    elif value == "close":
        loc_range = (2, 2, 5)
    else:
        raise Exception("something went wrong")
    bpy.ops.object.select_by_type(type="MESH")
    bpy.ops.object.randomize_transform(
        random_seed=random.randint(0, 999),
        loc=loc_range,
        rot=(0.3, 0.3, 0.3),
        scale_even=True,
        scale=(2, 2, 2),
    )
    bpy.ops.object.select_all(action="DESELECT")


def horizontal_origin_translator(value):
    if value == "far":
        bpy.data.cameras["Camera"].location[1] = -50
    elif value == "medium":
        pass
    elif value == "close":
        bpy.data.cameras["Camera"].location[1] = -20
    else:
        raise Exception("something went wrong")
    bpy.ops.object.select_all(action="DESELECT")


def vertical_origin_translator(value):
    if value == "up":
        bpy.data.cameras["Camera"].location[2] = -10
    elif value == "medium":
        pass
    elif value == "low":
        bpy.data.cameras["Camera"].location[2] = 10
    else:
        raise Exception("something went wrong")
    bpy.ops.object.select_all(action="DESELECT")


def lighting_type_translator(value):
    if value == "sun":
        return True
    elif value == "point":
        return False
    else:
        raise Exception("something went wrong")


def point_position_translator(value):
    bpy.ops.object.select_by_type(type="LIGHT")
    selection = bpy.context.selected_objects
    if value == "close":
        loc_range = (2, 2, 5)
    elif value == "medium":
        loc_range = (5, 5, 8)
    elif value == "far":
        loc_range = (7, 7, 10)
    else:
        raise Exception("something went wrong")
    bpy.ops.object.randomize_transform(
        random_seed=random.randint(0, 999), use_loc=True, loc=loc_range
    )
    bpy.ops.object.select_all(action="DESELECT")


def point_strength_translator(value):
    bpy.ops.object.select_by_type(type="LIGHT")
    selection = bpy.context.selected_objects
    if value == "strong":
        for point in selection:
            point.data.energy = random.randint(900, 1200)
    elif value == "medium":
        pass
    elif value == "weak":
        for point in selection:
            point.data.energy = random.randint(500, 800)
    else:
        raise Exception("something went wrong")
    bpy.ops.object.select_all(action="DESELECT")


def point_amount_translator(value):
    if value == "many":
        amount = 9
    elif value == "medium":
        amount = 3
    elif value == "few":
        amount = 1
    else:
        raise Exception("something went wrong")
    for i in range(amount):
        bpy.ops.object.light_add(type="POINT")
        point = bpy.context.active_object
        point.data.energy = random.randint(700, 1000)
        point.data.color = (1, 0.8, 0.5)
    bpy.ops.object.select_all(action="DESELECT")


def sun_direction_translator(value):
    bpy.ops.object.select_by_type(type="LIGHT")
    selection = bpy.context.selected_objects
    if value == "below":
        for sun in selection:
            sun.rotation_euler[0] = 3.14159
    elif value == "above":
        pass
    elif value == "frontal":
        for sun in selection:
            sun.rotation_euler[0] = 1.5708
    elif value == "lateral":
        for sun in selection:
            sun.rotation_euler[1] = random.choice([1.5708, -1.5708])
    else:
        raise Exception("something went wrong")
    bpy.ops.object.randomize_transform(
        random_seed=random.randint(0, 999),
        use_loc=False,
        use_rot=True,
        rot=(0.785398, 0.785398, 0.785398),
    )
    bpy.ops.object.select_all(action="DESELECT")


def sun_strength_translator(value):
    bpy.ops.object.select_by_type(type="LIGHT")
    selection = bpy.context.selected_objects
    if value == "strong":
        for sun in selection:
            sun.data.energy = 4
    elif value == "medium":
        pass
    elif value == "weak":
        for sun in selection:
            sun.data.energy = 2
    else:
        raise Exception("something went wrong")
    bpy.ops.object.select_all(action="DESELECT")


def sun_amount_translator(value):
    if value == "single":
        amount = 1
    elif value == "multiple":
        amount = 2
    else:
        raise Exception("something went wrong")
    for i in range(amount):
        bpy.ops.object.light_add(type="SUN")
        sun = bpy.context.active_object
        sun.data.energy = 3
        sun.data.color = (1, 0.8, 0.5)
    bpy.ops.object.select_all(action="DESELECT")


def translator(input_dict, path):
    sharpness_value = "sharp"
    shade_value = "medium"
    element_amount_value = "medium"
    element_concentration_value = "medium"
    horizontal_origin_value = "medium"
    vertical_origin_value = "medium"
    lighting_type_value = "sun"
    sun_direction_value = "above"
    sun_strength_value = "medium"
    sun_amount_value = "single"
    point_position_value = "medium"
    point_strength_value = "medium"
    point_amount_value = "medium"
    translation_parameter = input_dict["translation parameter"]
    if "sharpness" in translation_parameter:
        sharpness_value = translation_parameter["sharpness"]
    if "shade" in translation_parameter:
        shade_value = translation_parameter["shade"]
    if "element_amount" in translation_parameter:
        element_amount_value = translation_parameter["element_amount"]
    if "element_concentration" in translation_parameter:
        element_concentration_value = translation_parameter["element_concentration"]
    if "horizontal_origin" in translation_parameter:
        horizontal_origin_value = translation_parameter["horizontal_origin"]
    if "vertical_origin" in translation_parameter:
        vertical_origin_value = translation_parameter["vertical_origin"]
    if "lighting_type" in translation_parameter:
        lighting_type_value = translation_parameter["lighting_type"]
    if "sun_direction" in translation_parameter:
        sun_direction_value = translation_parameter["sun_direction"]
    if "sun_strength" in translation_parameter:
        sun_strength_value = translation_parameter["sun_strength"]
    if "sun_amount" in translation_parameter:
        sun_amount_value = translation_parameter["sun_amount"]
    if "point_position" in translation_parameter:
        point_position_value = translation_parameter["point_position"]
    if "point_strength" in translation_parameter:
        point_strength_value = translation_parameter["point_strength"]
    if "point_amount" in translation_parameter:
        point_amount_value = translation_parameter["point_amount"]
    sharpness_translator(sharpness_value)
    shade_translator(shade_value, input_dict)
    element_amount_translator(element_amount_value, path)
    element_concentration_translator(element_concentration_value)
    horizontal_origin_translator(horizontal_origin_value)
    vertical_origin_translator(vertical_origin_value)
    if lighting_type_translator(lighting_type_value):
        sun_amount_translator(sun_amount_value)
        sun_direction_translator(sun_direction_value)
        sun_strength_translator(sun_strength_value)
    else:
        point_amount_translator(point_amount_value)
        point_position_translator(point_position_value)
        point_strength_translator(point_strength_value)


clean_scene()
seed = set_seed(defined_seed=False)
path = "./"
input_dict = parse_input_data(path)
import_word(input_dict["word"])
setup_scene(input_dict["color_rgb"])
import_modules(input_dict["elements"], path)
translator(input_dict, path)
random_apply_materials()
render(path, input_dict["emotion"], seed)

