"""
This file includes commonly used utilities for this app.

"""

from datetime import datetime


today = datetime.now()
year = today.year
month = today.month
day = today.day

# Following are for images upload helper functions. The first two are used for product upload for the front and back.
# The last two are used for design product upload for the front and back.

def front_product_image(instance, filename):
    # file will be uploaded to MEDIA_ROOT/product_imgs/maker_<id>/product_<id>/Y/m/d/front/<filename>
    return 'product_imgs/maker_{0}/product_{1}/{2}/{3}/{4}/front/{5}'.format(instance.maker.id, instance.id, year, month, day, filename)

def back_product_image(instance, filename):
    # file will be uploaded to MEDIA_ROOT/product_imgs/maker_<id>/product_<id>/Y/m/d/back/<filename>
    return 'product_imgs/maker_{0}/product_{1}/{2}/{3}/{4}/back/{5}'.format(instance.maker.id, instance.id, year, month, day, filename)

def front_design_image(instance, filename):
    # file will be uploaded to MEDIA_ROOT/product_imgs/designer_<id>/design_product_<id>/Y/m/d/front/<filename>
    return 'product_imgs/designer_{0}/design_product_{1}/{2}/{3}/{4}/front/{5}'.format(instance.designer.id, instance.id, year, month, day, filename)

def back_design_image(instance, filename):
    # file will be uploaded to MEDIA_ROOT/product_imgs/designer_<id>/design_product_<id>/Y/m/d/back/<filename>
    return 'product_imgs/designer_{0}/design_product_{1}/{2}/{3}/{4}/back/{5}'.format(instance.designer.id, instance.id, year, month, day, filename)



def fill_category_tree(model, deep=0, parent_id=0, tree=[]):
    '''
    NAME::

        fill_category_tree

    DESCRIPTION::

        一般用来针对带有parent产品分类表字段的进行遍历，并生成树形结构

    PARAMETERS::

        :param model: 被遍历的model，具有parent属性
        :param deep: 本例中，为了明确表示父子的层次关系，用短线---的多少来表示缩进
        :param parent_id: 表示从哪个父类开始，=0表示从最顶层开始
        :param tree: 要生成的树形tuple

    RETURN::

        这里是不需要返回值的，但是如果某个调用中需要可以画蛇添足一下

    USAGE::

        调用时，可以这样：
        choices = [()]
        fill_topic_tree(choices=choices)
        这里使用[],而不是()，是因为只有[]，才能做为“引用”类型传递数据。
    '''
    if parent_id == 0:
        ts = model.objects.filter(parent = None)
#        tree[0] += ((None, '选择产品类型'),)
        for t in ts:
            tmp = [()]
            fill_category_tree(4, t.id, tmp)
            tree[0] += ((t.id, '-'*deep + t.name,),)
            for tt in tmp[0]:
                tree[0] += (tt,)
    else:
        ts = Category.objects.filter(parent_id = parent_id)
        for t in ts:
            tree[0] += ((t.id, '-'*deep + t.name,),)
            fill_category_tree(deep + 4, t.id, tree)

    return tree