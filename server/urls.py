from fastapi import APIRouter

from server import views

router = APIRouter()

router.add_api_route('/Login', views.Login, methods=['post'])
router.add_api_route('/SignUp', views.SignUp, methods=['post'])
router.add_api_route('/getUserInfo', views.getUserInfo, methods=['post'])
router.add_api_route('/getOperateOps', views.getOperateOps, methods=['get'])
router.add_api_route('/changePassword', views.changePassword, methods=['post'])
router.add_api_route('/setAvatar', views.setAvatar, methods=['post'])
router.add_api_route('/overview', views.overview, methods=['post'])
router.add_api_route('/chartData', views.chartData, methods=['get'])
router.add_api_route('/chartData2', views.chartData2, methods=['get'])

router.add_api_route('/toFocusProj', views.toFocusProj, methods=['get'])
router.add_api_route('/toFocusDevUser', views.toFocusDevUser, methods=['get'])
router.add_api_route('/getFocusArr', views.getFocusArr, methods=['get'])
router.add_api_route('/Soul', views.Soul, methods=['get'])
router.add_api_route('/Upload', views.Upload, methods=['post'])

router.add_api_route('/getRoleList', views.getRoleList, methods=['get'])
router.add_api_route('/addRole', views.addRole, methods=['post'])
router.add_api_route('/deleteRole', views.deleteRole, methods=['get'])
router.add_api_route('/getUserList', views.getUserList, methods=['get'])
router.add_api_route('/addUser', views.addUser, methods=['post'])
router.add_api_route('/updateRole', views.updateRole, methods=['post'])
router.add_api_route('/updateUser', views.updateUser, methods=['post'])
router.add_api_route('/deleteUser', views.deleteUser, methods=['get'])

# 项目管理路由
router.add_api_route('/getProjectList', views.getProjectList, methods=['get'])
router.add_api_route('/addProject', views.addProject, methods=['post'])
router.add_api_route('/updateProject', views.updateProject, methods=['post'])
router.add_api_route('/deleteProject', views.deleteProject, methods=['get'])

# 开发者管理路由
router.add_api_route('/getDevUserList', views.getDevUserList, methods=['get'])
router.add_api_route('/addDevUser', views.addDevUser, methods=['post'])
router.add_api_route('/updateDevUser', views.updateDevUser, methods=['post'])
router.add_api_route('/deleteDevUser', views.deleteDevUser, methods=['get'])
