# Copyright (C) 2020-2025 Motphys Technology Co., Ltd. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import pathlib
import os

from motrixsim import SceneData, msd, run, step, viewer
from motrixsim.render import RenderApp
import motrixsim

# motrixsim.

# RESOURCE_DIR = pathlib.Path(__file__).parent.parent / "resource"
SCENE_XML = "resource/common/flat_scene.xml"
VEHICLE_XML = "resource/nio_es6.xml"

# 添加 ABS PATH
SCENE_XML = os.path.abspath(SCENE_XML)
VEHICLE_XML = os.path.abspath(VEHICLE_XML)

print(SCENE_XML)
print(VEHICLE_XML)

# 设置环境变量
# RUST_BACKTRACE=1
os.environ["RUST_BACKTRACE"] = "full"



def main():
    view_mode:int = 2

    # =============================================================
    # 第一步：加载场景和车辆模型
    # msd (MuJoCo Scene Description) 采用声明式 API
    # scene: 包含地面、光照等环境元素
    # vehicle: 包含车身、4个轮子刚体及其关节
    # =============================================================
    scene = msd.from_file(str(SCENE_XML))
    vehicle = msd.from_file(str(VEHICLE_XML))

    # =============================================================
    # 第二步：将车辆装配到场景中，并构建物理模型
    # vehicle 的 worldbody 内容会附加到 scene 的 worldbody 下
    # =============================================================
    scene.attach(vehicle)
    model = scene.build()
    data = SceneData(model)

    # =============================================================
    # 第三步：创建仿真数据容器和渲染窗口
    # data: 存储物理仿真状态（位置、速度、力等）
    # render: 3D 可视化窗口，同步物理状态到图形渲染
    # =============================================================
    
    if (view_mode == 1):
        with RenderApp(log_level="info") as render:
            render.launch(model)
            # data = SceneData(model)

            def phys_step():
                model.step(data)

            def render_step():
                render.sync(data)

            def on_click():
                print("Button clicked!")

            def on_toggle_changed(value: bool):
                print("toggle value:", value)

            render.opt.set_left_panel_vis(True)
            render.ui.add_button("Click Me", on_click)
            render.ui.add_toggle("Some Toggle", False, on_toggle_changed)

            run.render_loop(
                model.options.timestep,
                60,
                phys_step,
                render_step,
            )
    elif (view_mode == 2):
        viewer.launch(model, data)


if __name__ == "__main__":
    main()
