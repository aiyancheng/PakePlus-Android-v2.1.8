import os, sys
sys.stdout.reconfigure(encoding='utf-8')

base = r'c:\Users\81784\WorkBuddy\20260326092633\眼镜门店新员工8周成才'

def add_home_button(filepath):
    """在导航区中间增加返回首页按钮"""
    with open(filepath, encoding='utf-8') as f:
        c = f.read()
    
    # 查找导航部分
    nav_start = c.find('<div class="nav-footer"')
    if nav_start == -1:
        # 可能是练习题文件，导航样式不同
        nav_start = c.find('<div class="nav-footer')
        if nav_start == -1:
            # 练习题文件 nav-footer 可能没引号
            nav_start = c.find('<div class=nav-footer')
    
    if nav_start == -1:
        print(f"  ❌ {os.path.basename(filepath)}: 未找到 nav-footer")
        return False
    
    nav_end = c.find('</div>', nav_start) + 6
    nav_section = c[nav_start:nav_end]
    
    # 判断文件类型和学习内容还是练习题
    is_content = '_学习内容.html' in filepath
    is_practice = '_练习题.html' in filepath
    
    # 中间按钮：返回首页
    home_btn = '<a class="nav-btn outline" href="../index.html">🏠 首页</a>'
    
    # 如果是学习内容文件，通常在两个按钮之间
    if is_content:
        # 找到第二个a标签的位置
        second_a = nav_section.find('</a>')
        second_a_end = nav_section.find('>', second_a + 4)
        if second_a != -1:
            new_nav = nav_section[:second_a+4] + '\n    ' + home_btn + '\n    ' + nav_section[second_a+4:]
        else:
            # 后备方案：直接插入在第一个按钮后
            new_nav = nav_section.replace('</a>', f'</a>\n    {home_btn}')
    
    # 如果是练习题文件，通常是一个按钮
    elif is_practice:
        # 找到按钮位置，插入home按钮
        first_btn_end = nav_section.find('</a>')
        if first_btn_end != -1:
            new_nav = nav_section[:first_btn_end+4] + '\n    ' + home_btn + '\n    ' + nav_section[first_btn_end+4:]
        else:
            # 后备方案：直接添加
            new_nav = nav_section.replace('</div>', f'\n    {home_btn}\n  </div>')
    
    else:
        # 默认处理：在现有按钮之间插入
        first_btn_end = nav_section.find('</a>')
        if first_btn_end != -1:
            new_nav = nav_section[:first_btn_end+4] + '\n    ' + home_btn + '\n    ' + nav_section[first_btn_end+4:]
        else:
            new_nav = nav_section.replace('</div>', f'\n    {home_btn}\n  </div>')
    
    new_c = c[:nav_start] + new_nav + c[nav_end:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_c)
    
    return True

def process_week(week_dir):
    """处理一周内的所有文件"""
    count_ok = 0
    count_fail = 0
    
    week_name = os.path.basename(week_dir)
    print(f'处理 {week_name} ...')
    
    for fname in sorted(os.listdir(week_dir)):
        if fname.endswith('.html') and ('Day' in fname or '总览' in fname):
            fp = os.path.join(week_dir, fname)
            if add_home_button(fp):
                count_ok += 1
            else:
                count_fail += 1
    
    return count_ok, count_fail

# 处理课程总览
index_file = os.path.join(base, 'index.html')
if os.path.exists(index_file):
    print('处理 index.html ...')
    add_home_button(index_file)

# 处理课程总览.html
if os.path.exists(os.path.join(base, '课程总览.html')):
    print('处理 课程总览.html ...')
    add_home_button(os.path.join(base, '课程总览.html'))

# 处理8周目录
weeks = [
    "第1周_文化与制度启蒙",
    "第2周_光学与产品知识",
    "第3周_专业技能训练",
    "第4周_销售话术与中期考核",
    "第5周_实战跟岗训练",
    "第6周_独立接单训练",
    "第7周_综合提升训练",
    "第8周_结业冲刺与毕业考核",
]

total_ok, total_fail = 0, 0
for week in weeks:
    week_dir = os.path.join(base, week)
    if os.path.exists(week_dir):
        ok, fail = process_week(week_dir)
        total_ok += ok
        total_fail += fail

print(f'\n总计处理 {total_ok} 个文件成功, {total_fail} 个文件失败')
