import glob

def load_img_path_list(load_path):
    person_list = []
    with open(load_path, 'r') as f:
        for line in f:
            person_data = line.strip()
            person_list.append(person_data)
    return person_list


img_path_list = glob.glob("./image/baseball/*/*/*/*.jpg")
#img_path_list = glob.glob("./image/baseball/*/*/*")

#img_path_list = glob.glob("./image/football/*/*/*/*.jpg")
#img_path_list = glob.glob("./image/football/*/*/*")
print(len(img_path_list))


begin_age = 40
end_age = 49
img_num = 0
for age in range(begin_age, end_age+1):
    load_path = "./data/baseball_image_path_list_age" + str(age) + ".txt"
    #load_path = "./data/football_image_path_list_age" + str(age) + ".txt"
    #load_path = "./data/football_image_path_list_age" + str(age) + "_origin.txt"
    img_path_list = load_img_path_list(load_path)
    img_num += len(img_path_list)
print(img_num)