
# 学生管理应用 - CI 构建镜像到 GHCR 完整流程

---

# 1. 项目结构

```
your-project/
├── .github/
│   └── workflows/
│       └── docker-build.yml    # CI 自动化脚本
├── Dockerfile                  # 构建镜像用
├── main.py                     # 你的 Python 学生管理代码
└── README.md                   # 本说明
```

---

# 2. 前置准备：创建 GitHub Token（必须做）

## 2.1 创建 PAT（Personal Access Token）

1. 打开 GitHub → 右上角头像 → **Settings**
2. 左侧最下方 → **Developer settings**
3. **Personal access tokens** → **Tokens (classic)**
4. **Generate new token (classic)**
5. 配置：
   - Note：`GHCR_TOKEN`
   - Expiration：90 days
   - 勾选权限：**`write:packages`**
6. 点 **Generate token**
7. **复制生成的 token 字符串（只显示一次！）**

## 2.2 把 Token 存入仓库 Secrets

1. 进入你的 GitHub 仓库
2. **Settings → Secrets and variables → Actions**
3. **New repository secret**
   - Name：`GHCR_TOKEN`
   - Secret：粘贴刚才复制的 token
4. 保存

---

# 3. 必须的 3 个文件内容（直接复制）

## 3.1 Dockerfile（根目录）

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
CMD ["python", "main.py"]
```

## 3.2 .github/workflows/docker-build.yml（CI 核心）

```yaml
# .github/workflows/docker-build.yml
name: Build and Push Docker Image to GHCR

# 触发规则：推送到main分支、打版本tag、手动触发都可以执行
on:
  push:
    branches: [ "main" ]
    tags: [ 'v*' ]
  workflow_dispatch: # 允许在GitHub页面手动触发构建

# 全局环境变量，无需修改，自动适配你的GitHub账号
env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository_owner }}/student-app

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
      id-token: write

    steps:
      # 1. 拉取仓库代码
      - name: Checkout repository
        uses: actions/checkout@v4

      # 2. 设置Docker Buildx，支持多架构镜像+构建缓存
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      # 3. 登录到GHCR容器仓库
      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GHCR_TOKEN }}

      # 4. 自动生成镜像标签和元数据
      - name: Extract Docker metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=tag
            type=sha,format=short,prefix=

      # 5. 构建并推送Docker镜像
      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## 3.3 main.py

```python
class Student:
    def __init__(self, name: str, age: int, student_id: str) -> None:
        self.name = name.strip()
        self.age = age
        self.student_id = student_id.strip()

    def __repr__(self) -> str:
        return f"Student(name={self.name!r}, age={self.age}, student_id={self.student_id!r})"


def get_valid_age(prompt: str) -> int:
    while True:
        age_input = input(prompt).strip()
        if not age_input:
            print("Age cannot be empty. Please try again.")
            continue
        if not age_input.isdigit():
            print("Please enter a valid number for age.")
            continue

        age = int(age_input)
        if age <= 0:
            print("Age must be greater than zero.")
            continue

        return age


def collect_student_data(count: int = 3) -> list[Student]:
    students: list[Student] = []

    print(f"Please enter information for {count} students.")
    for index in range(1, count + 1):
        print(f"\nStudent {index}")
        name = input("  Name: ").strip()
        while not name:
            print("  Name cannot be empty.")
            name = input("  Name: ").strip()

        age = get_valid_age("  Age: ")

        student_id = input("  Student ID: ").strip()
        while not student_id:
            print("  Student ID cannot be empty.")
            student_id = input("  Student ID: ").strip()

        students.append(Student(name, age, student_id))

    return students


def print_students_sorted(students: list[Student]) -> None:
    print("\nStudent names and ages in order:")
    for student in sorted(students, key=lambda s: s.name.lower()):
        print(f"- {student.name}, {student.age} years old")


if __name__ == "__main__":
    student_list = collect_student_data(3)
    print_students_sorted(student_list)
```

---

# 4. CI 完整流程

## 4.1 你只需要做一件事

**把代码提交并推送到 GitHub main 分支**

```bash
git add .
git commit -m "add CI workflow"
git push origin main
```

## 4.2 GitHub 自动做什么（CI 流程）

1. 代码 push → 触发 GitHub Action
2. 拉取代码
3. 准备 Docker 环境
4. 登录 GHCR 镜像仓库
5. **自动构建 Docker 镜像**
6. **自动推送到 GHCR（GitHub 容器仓库）**
7. 完成 ✅

## 4.3 查看是否成功

1. 打开仓库 → **Actions**
2. 看任务是否全绿
3. 绿 = 镜像已构建并推送到 GHCR

## 4.4 查看镜像位置

GitHub 头像 → **Packages**
就能看到 `student-app` 镜像

---

# 5. 镜像名称规则

```
ghcr.io/你的GitHub用户名/student-app:main
```

例子：

```
ghcr.io/zhangsan/student-app:main
```

---

# 6. 明天你可以直接问我的内容（你可以写在 README 末尾）

- 如何在 K3s 里拉取这个镜像并运行？
- 如何接入 Argo CD 实现自动部署（CD）？
- 如何让 CI 自动更新 Argo CD 的镜像版本？

---

## 明天你起床直接用这份 README

**不用改任何东西，直接提交到 GitHub，CI 就会自动跑！**
你现在的 Python 代码完全不用动，CI 流程 100% 兼容。
