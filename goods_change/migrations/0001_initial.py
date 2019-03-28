# Generated by Django 2.0.7 on 2018-09-29 15:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsColorChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gcc_id', models.UUIDField(default=uuid.UUID('828cf974-c3b5-11e8-9c02-005056c00008'))),
                ('gcc_change_color_num', models.IntegerField()),
                ('gcc_change_color_state', models.IntegerField(choices=[(0, '不变'), (1, '上升'), (2, '下降')], default=0)),
                ('gcc_time', models.DateField()),
                ('create_date', models.DateField(auto_now_add=True)),
                ('create_end_date', models.DateField(auto_now=True)),
                ('isdelete', models.BooleanField(default=False)),
                ('gcc_now_goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='now_goods', to='goods.Goods')),
                ('gcc_previous_goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gcc_previous_goods', to='goods.Goods')),
            ],
            options={
                'verbose_name': '产品颜色变化',
                'verbose_name_plural': '产品颜色变化',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='GoodsColorChangeColor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gccc_id', models.UUIDField(default=uuid.UUID('828cf975-c3b5-11e8-8945-005056c00008'))),
                ('gccc_color', models.CharField(max_length=100)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('create_end_date', models.DateField(auto_now=True)),
                ('isdelete', models.BooleanField(default=False)),
                ('gccc_goodscolorchange', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods_change.GoodsColorChange')),
            ],
            options={
                'verbose_name': '产品颜色变化的颜色',
                'verbose_name_plural': '产品颜色变化的颜色',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='GoodsExtenceChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gec_id', models.UUIDField(default=uuid.UUID('828cab53-c3b5-11e8-be58-005056c00008'))),
                ('gec_extence_type', models.IntegerField(choices=[(0, '不变'), (1, '下架'), (2, '上架')], default=0)),
                ('gec_extence_now_time', models.DateField()),
                ('gec_extence_before_time', models.DateField()),
                ('create_date', models.DateField(auto_now_add=True)),
                ('create_end_date', models.DateField(auto_now=True)),
                ('isdelete', models.BooleanField(default=False)),
                ('gec_extence_goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Goods')),
            ],
            options={
                'verbose_name': '产品上下架变化',
                'verbose_name_plural': '产品上下架变化',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='GoodsOrderChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goc_id', models.UUIDField(default=uuid.UUID('828cd264-c3b5-11e8-887f-005056c00008'))),
                ('goc_now_time', models.DateField()),
                ('goc_before_time', models.DateField()),
                ('create_date', models.DateField(auto_now_add=True)),
                ('create_end_date', models.DateField(auto_now=True)),
                ('isdelete', models.BooleanField(default=False)),
                ('goc_now_goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goc_now_goods', to='goods.Goods')),
                ('goc_previous_goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goc_previous_goods', to='goods.Goods')),
            ],
            options={
                'verbose_name': '产品网站位置品牌',
                'verbose_name_plural': '产品网站位置品牌',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='GoodsOrderChangeChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gocc_id', models.UUIDField(default=uuid.UUID('828cd265-c3b5-11e8-9789-005056c00008'))),
                ('gocc_now_goods_id', models.CharField(max_length=50)),
                ('gocc_previous_order', models.IntegerField()),
                ('gocc_now_order', models.IntegerField()),
                ('gocc_order_change', models.CharField(max_length=20)),
                ('gocc_order_state', models.IntegerField(choices=[(0, '不变'), (1, '上升'), (2, '下降')], default=0)),
                ('gocc_sex', models.CharField(max_length=20)),
                ('gocc_page', models.IntegerField(default=1)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('create_end_date', models.DateField(auto_now=True)),
                ('isdelete', models.BooleanField(default=False)),
                ('goocc_goc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods_change.GoodsOrderChange')),
            ],
            options={
                'verbose_name': '产品网站位置变化',
                'verbose_name_plural': '产品网站位置变化',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='GoodsPriceChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gpc_id', models.UUIDField(default=uuid.UUID('828cab52-c3b5-11e8-8528-005056c00008'))),
                ('gpc_price_type', models.CharField(default='$', max_length=10)),
                ('gpc_previous_price', models.CharField(max_length=20)),
                ('gpc_now_price', models.CharField(max_length=20)),
                ('gpc_price_change', models.CharField(max_length=20)),
                ('gpc_price_state', models.IntegerField(choices=[(0, '不变'), (1, '上升'), (2, '下降')], default=0)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('create_end_date', models.DateField(auto_now=True)),
                ('isdelete', models.BooleanField(default=False)),
                ('gpc_now_goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gpc_now_goods', to='goods.Goods')),
                ('gpc_previous_goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gpc_previous_goods', to='goods.Goods')),
                ('gpc_time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Time')),
            ],
            options={
                'verbose_name': '产品价格变化',
                'verbose_name_plural': '产品价格变化',
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='ProductAnalysisConfirmation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pac_id', models.UUIDField(default=uuid.UUID('828c8442-c3b5-11e8-8712-005056c00008'))),
                ('pac_brand', models.CharField(max_length=100)),
                ('pac_type', models.CharField(max_length=50)),
                ('pac_before_time', models.DateField()),
                ('pac_now_time', models.DateField()),
                ('create_date', models.DateField(auto_now_add=True)),
                ('create_end_date', models.DateField(auto_now=True)),
                ('isdelete', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': '产品分析确认',
                'verbose_name_plural': '产品分析确认',
                'ordering': ['pk'],
            },
        ),
    ]
