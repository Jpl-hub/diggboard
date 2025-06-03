import {instance} from "@/api/base";


export const Login = async (data) => {
    return await instance.post('/Login', data)
}

export const SignUp = async (data) => {
    return await instance.post('/SignUp', data)
}


export const changePassword = async (data) => {
    return await instance.post('/changePassword', {}, {params: data})
}

export const setAvatar = async (data) => {
    return await instance.post('/setAvatar', {}, {params: data})
}


export const getUserInfo = async (data) => {
    return await instance.post('/getUserInfo', data)
}

export const getOperateOps = async (data) => {
    return await instance.get('/getOperateOps', {params: data})
}


export const overview = async (data) => {
    return await instance.post('/overview', data)
}

export const toFocusProj = async (data) => {
    return await instance.get('/toFocusProj', {params: data})
}
export const toFocusDevUser = async (data) => {
    return await instance.get('/toFocusDevUser', {params: data})
}

export const getFocusArr = async (data) => {
    return await instance.get('/getFocusArr', {params: data})
}


export const chartData = async (data) => {
    return await instance.get('/chartData', {params: data})
}
export const chartData2 = async (data) => {
    return await instance.get('/chartData2', {params: data})
}

export const Soul = async (data) => {
    return await instance.get('/Soul', {params: data})
}

export const getRoleList = async (data) => {
    return await instance.get('/getRoleList', {params: data})
}

export const addRole = async (data) => {
    return await instance.post('/addRole', data)
}

export const deleteRole = async (data) => {
    return await instance.get('/deleteRole', {params: data})
}

export const updateRole = async (data) => {
    return await instance.post('/updateRole', data)
}


export const getUserList = async (data) => {
    return await instance.get('/getUserList', {params: data})
}

export const addUser = async (data) => {
    return await instance.post('/addUser', data)
}

export const updateUser = async (data) => {
    return await instance.post('/updateUser', data)
}


export const deleteUser = async (data) => {
    return await instance.get('/deleteUser', {params: data})
}

// 项目管理相关接口
export const getProjectList = async (data) => {
    return await instance.get('/getProjectList', {params: data})
}

export const addProject = async (data) => {
    return await instance.post('/addProject', data)
}

export const updateProject = async (data) => {
    return await instance.post('/updateProject', data)
}

export const deleteProject = async (data) => {
    return await instance.get('/deleteProject', {params: data})
}

// 开发者管理相关接口
export const getDevUserList = async (data) => {
    return await instance.get('/getDevUserList', {params: data})
}

export const addDevUser = async (data) => {
    return await instance.post('/addDevUser', data)
}

export const updateDevUser = async (data) => {
    return await instance.post('/updateDevUser', data)
}

export const deleteDevUser = async (data) => {
    return await instance.get('/deleteDevUser', {params: data})
}


































