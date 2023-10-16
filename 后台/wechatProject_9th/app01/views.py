from django.shortcuts import render,HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from ext.auth import RecordAuthentication


# Create your views here.
def index(request):
    return HttpResponse('欢迎使用')


from rest_framework.viewsets import ModelViewSet
from .models import User,Record
from .serializers import UserModelSerializer, LoginSerializers, RecordSerializers
import uuid

# Create your views here.
# class UserViewSet(ModelViewSet):
#     queryset = User.objects.all()       # queryset 指明该视图集在查询数据时使用的查询集
#     serializer_class = UserModelSerializer # 指明该视图在进行序列化或反序列化时使用的序列化器


class UserView(APIView):
    """获取全部用户、用户注册"""
    def get(self, request):
        """获取全部用户"""
        users = User.objects.all()
        # 将数据从数据库取出序列化后传给前端
        user_serializer=UserModelSerializer(users, many=True)
        return Response({
            'status': '200',
            'msg': 'ok',
            'results': user_serializer.data
        })

    def post(self,request):
        """新建用户"""
        # 获取到前端的数据先校验
        user = UserModelSerializer(data=request.data)
        # {"username":"5","password":"6"}
        # User.objects.create(user)

        #print(user.is_valid())
        #print(user.data) # JSON格式：{'username': '5', 'password': '6'}

        if user.is_valid():
            user.validated_data.pop("confirm_password")
            user.save()
            return Response({
                'status': '200',
                'msg': '注册成功！'
            })

        return Response({
            'status': '500',
            'msg': user.errors
        })


class LoginView(APIView):
    """登录、修改密码（待完善！！！）"""
    authentication_classes = [RecordAuthentication, ]

    def post(self, request):
        ser = LoginSerializers(data=request.data)
        if not ser.is_valid():
            return Response({
                'status': '500',
                'msg': ser.errors
            })
        user = User.objects.filter(**ser.validated_data).first()
        if not user:
            return Response({
                'status': '500',
                'msg': "用户名或密码错误"
            })
        token = str(uuid.uuid4())
        user.token=token
        user.save()

        return Response({
            'status': '200',
            'msg': '登录成功！',
            # 'data': {
            #     'userInfo': user
            # }
            'user': {
                'username': user.username,
                'token': user.token
            }
        })

    def put(self,request):
        # 密码修改（需登录）
        # 没使用confirm_new_password二次确认密码
        # # 查看用户是否登录，但不用登录也可以修改密码
        # if not request.user:
        #     return Response({
        #         'status': '500',
        #         'msg': '认证失败'
        #     })
        print(request.data)     # {'username': 'test', 'password': '111', 'new_password': '121', 'confirm_new_password': '121'}
        # 验证用户书写格式是否正确
        ser = LoginSerializers(data=request.data)
        if not ser.is_valid():
            return Response({
                'status': '500',
                'msg': ser.errors
            })
        # 验证用户旧密码是否正确
        user = User.objects.filter(**ser.validated_data).first()
        if not user:
            return Response({
                'status': '500',
                'msg': "用户名或密码错误"
            })
        new_password=request.data.get('new_password')
        user.password=new_password
        user.save()
        return Response({
            'status': '200',
            'msg': '修改成功！'
        })


class RecordView(APIView):
    """查看所有记录、新增记录（没写完）！！！"""
    authentication_classes = [RecordAuthentication, ]

    def get(self, request):
        """获取所有收支记录"""
        # 查看用户是否登录
        if not request.user:
            return Response({
                'status': '500',
                'msg': '认证失败'
            })
        # 获取数据库中该用户的所有手机记录
        userid = request.user.id
        print(request.user.id)
        records = Record.objects.filter(user=userid)

        ser = RecordSerializers(instance=records, many=True)
        return Response({
            'status': '200',
            'msg': 'ok',
            'results': ser.data
        })

    def post(self, request):
        """新增收支记录"""
        userid = request.user.id
        print(request.data)
        return Response({
            'status': '200',
            'msg': 'ok',
            'results': "ser.data"
        })


class RecordDetailView(APIView):
    """单条记录的修改、删除"""
    authentication_classes = [RecordAuthentication, ]

    def put(self, request, record_id):
        """添加/修改备注"""
        if not request.user:
            return Response({
                'status': '500',
                'msg': '认证失败'
            })

        userid = request.user.id
        record = Record.objects.filter(id=record_id).first()
        if not record:
            return Response({
                'status': '500',
                'msg': '没有该记录，请刷新'
            })
        note=request.data.get("note")
        record.note=note
        record.save()

        return Response({
            'status': '200',
            'msg': '修改成功！'
        })

    def delete(self, request, record_id):
        """删除备注"""
        if not request.user:
            return Response({
                'status': '500',
                'msg': '认证失败'
            })
        Record.objects.filter(id=record_id).delete()
        return Response({
            'status': '200',
            'msg': '修改成功！'
        })

class RecordYearView(APIView):
    authentication_classes = [RecordAuthentication, ]

    def get(self, request, condition, num, category):
        """按年/月/日查询，类别。要修改，按范围查询写到一起了，但写到一起后按范围查询就不能同时按类别查询了"""
        if not request.user:
            return Response({
                'status': '500',
                'msg': '认证失败'
            })
        userid=request.user.id
        if(condition == "year"):
            records = Record.objects.filter(user=userid).filter(ctime__year=int(num))
            print(records)
        elif(condition == "month"):
            records = Record.objects.filter(user=userid).filter(ctime__month=int(num))
        elif (condition == "day"):
            records = Record.objects.filter(user=userid).filter(ctime__day=int(num))
        elif(condition=="range"):
            records=Record.objects.filter(user=userid).filter(ctime__range=(num,category))

        if(condition!="range" and category!="all"):
            records = records.filter(category=category)

        ser = RecordSerializers(instance=records, many=True)
        return Response({
            'status': '200',
            'msg': '修改成功！',
            'results': ser.data
        })
