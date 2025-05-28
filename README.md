# Dashboard 项目

这是一个前后端分离的数据看板项目，前端使用 Vue 3 + Vite，后端使用 Python (Flask/FastAPI)。

## 环境配置

### 1. 环境变量设置

项目使用环境变量管理敏感信息。请按以下步骤配置：

1. 复制环境变量示例文件：
   ```bash
   cp env.example .env
   ```

2. 编辑 `.env` 文件，填入你的实际配置：
   ```
   # 数据库配置
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_NAME=your_db_name

   # JWT配置
   JWT_SECRET_KEY=your_secret_key_here
   JWT_ALGORITHM=HS256
   JWT_EXPIRE_HOURS=30

   # GitHub API配置
   GITHUB_TOKEN=your_github_token_here

   # 前端API配置
   VITE_API_BASE_URL=http://127.0.0.1:7878
   VITE_UPLOAD_URL_DEV=http://127.0.0.1:7777/api/Upload
   VITE_UPLOAD_URL_PROD=https://your-domain.com/upload
   VITE_REDIRECT_URL=https://your-redirect-url.com
   ```

### 2. 后端安装

1. 创建虚拟环境：
   ```bash
   python -m venv venv
   ```

2. 激活虚拟环境：
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. 安装依赖：
   ```bash
   cd server
   pip install -r req.txt
   ```

4. 运行后端服务：
   ```bash
   python main.py
   ```

### 3. 前端安装

1. 安装依赖：
   ```bash
   pnpm install
   ```

2. 运行开发服务器：
   ```bash
   pnpm dev
   ```

3. 构建生产版本：
   ```bash
   pnpm build
   ```

## 注意事项

- **不要将 `.env` 文件提交到版本控制系统**
- 确保所有敏感信息都通过环境变量管理
- 生产环境部署时，请使用强密码和安全的密钥

## 项目结构

```
dash_board/
├── server/          # 后端代码
├── src/             # 前端源码
├── venv/            # Python虚拟环境
├── .env             # 环境变量文件（不提交）
├── env.example      # 环境变量示例
└── README.md        # 本文件
```

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
