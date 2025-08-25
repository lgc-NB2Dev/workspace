<!-- markdownlint-disable MD033 -->

# Workspace

开发 NoneBot2 插件的工作区

## 开发

### 克隆 & 依赖安装

使用以下命令来克隆本工作区进行插件开发

```bash
git clone --recursive --depth=1 https://github.com/lgc-NB2Dev/workspace
```

使用 `uv` 来安装工作区内所有插件及其依赖到当前环境中

```bash
uv sync -U
```

### 配置调试环境

使用环境中的 `nb-cli` 与 `nb-cli-plugin-bootstrap` 创建一个测试用的 NoneBot2 项目

```bash
cd private && nb bs
```

运行上方命令进入创建向导之后，项目名称填写 `test-nb2`，不要创建虚拟环境，其他按需要选择即可

你也可以使用 `nb init` 来创建，不过创建项目后可能需要你手动生成 `bot.py`

创建好之后自行安装需要的依赖到当前环境中即可

配置好后使用 VSCode 的“运行和调试”标签页和“Run TestNB2”运行项来启动 NoneBot2

如果想要测试工作区内的插件，在 bot 项目的 `pyproject.toml` 中的 `tool.nonebot.plugins` 项中添加插件的包名即可

## 联系我

QQ：3076823485  
吹水群：[168603371](https://qm.qq.com/q/EikuZ5sP4G)  
邮箱：<lgc2333@126.com>

## 赞助

**[赞助我](https://blog.lgc2333.top/donate)**

感谢大家的赞助！你们的赞助将是我继续创作的动力！
