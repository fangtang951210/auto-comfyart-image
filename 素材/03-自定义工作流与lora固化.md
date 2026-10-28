# 素材03:自定义工作流与 lora 固化(实测)

## 自定义工作流四步(MCP 通道)
1. **标记**:API 格式工作流(ComfyUI 里 工作流→导出API)给节点加标题标记:@prompt(提示词节点)/@size(宽高节点)/@image(载图)/@unet(底模,可选,lora 挂点)/@save(多末端时)
2. **check**:custom_workflow action=check 验证标记
3. **install**:action=install + name + feature(generate/style/edit…),文件存 `comfyart/workflows/<feature>/`
4. **assign**:切换当前生效文件(生成槽=模型切换器;file:"" 回内置)

## lora 的两个世界
- **UI 原生**:生成卡片→高级→添加LoRA(选/换/删)。运行时把 LoraLoaderModelOnly 串在 @unet 节点后(源码 applyLoras)。**MCP 的 generate_image 没有 lora 参数**(schema 无、update_shapes 进不了卡片 meta)——上游缺口
- **固化方案(实测✅)**:把 lora 直接写进工作流(LoraLoaderModelOnly 固定 name+strength,串 UNET→Lora→KSampler),一个组合一个文件,靠 assign 切换。实测 image_00041 = darkBeast330 + krea2_beautiful@1.0,MCP 两步直达

## 现役图片工作流(本机)
| 槽 | assigned | 档案库 |
|---|---|---|
| generate | 风格化文生图(darkBeast+beautiful) | Krea2-Turbo(素)/ MOSS |
| style | 图生图(Krea2,TextEncodeQwenImageEditPlus 吃 image1) | — |

## 命名细节
- 文件名即显示名(label=file 去后缀);改名=改文件名+重新 assign(旧 assign 失效会自动回内置)
- 围挡分支名带 git 用户名前缀(github 场景注意)
