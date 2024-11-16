keyword = '给我来七张r18，裸足，萝莉瑟图'
start_word = '给我来'
setu_keyword = ['色图', 'setu', '涩图', '瑟图']
r18 = 0
if keyword.startswith(start_word):
    hanzi_quantity = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
    quantity = keyword.split(start_word)[1][0]
    if quantity not in hanzi_quantity:
        quantity = 1
    elif quantity in hanzi_quantity:
        quantity = hanzi_quantity.index(quantity) + 1
    num = quantity
    # 从文本中找出"张"与sufix之间的文本
    sufix = [i for i in setu_keyword if i in keyword][-1]
    first_proc = keyword.split('张')[1]
    second_proc = first_proc.split(sufix)[0]
    tag = second_proc.split('，')
    if 'r18' in tag:
        r18 = 1
        tag.remove('r18')
    if len(tag) != 0:
        # 把tag中的每个元素包装成一个单独的列表，并把这些列表放在一个列表中
        tag = [[i] for i in tag]

    print(tag)
    print(num)
    print(r18)
