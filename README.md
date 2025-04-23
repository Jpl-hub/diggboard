## 本地部署与运行

1. **安装依赖**

   前端：进入 `src` 目录，执行  
     ```sh
     pnpm install
     ```
   后端：进入 `server` 目录，执行  
     ```sh
     pip install -r req.txt
     ```

3. **启动数据库服务**  
   创建名为 `dashboard` 的数据库，可替换成自己密码
4. **生成测试数据**  
   运行后端提供的数据生成脚本，批量生成测试数据
5. **启动后端服务**  
   在 `server` 目录下运行：
   ```sh
   uvicorn server.main:fast_app --reload --port 7878
   ```

6. **启动前端服务**  
   在 `src` 目录下运行：
   ```sh
   pnpm dev

7. **访问系统**  
   打开浏览器访问前端地址 [http://localhost:7777](http://localhost:7777) 即可使用。


如有问题请及时沟通！
