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

from motrixsim import SceneData, msd, run, step
from motrixsim.render import RenderApp
import motrixsim

# motrixsim.

# RESOURCE_DIR = pathlib.Path(__file__).parent.parent / "resource"
SCENE_XML = "resource/common/flat_scene.xml"
VEHICLE_XML = "resource/nio_es6.xml"

print(SCENE_XML)
print(VEHICLE_XML)


def main():

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

    # =============================================================
    # 第三步：创建仿真数据容器和渲染窗口
    # data: 存储物理仿真状态（位置、速度、力等）
    # render: 3D 可视化窗口，同步物理状态到图形渲染
    # =============================================================
    with RenderApp() as render:
        render.launch(model)
        data = SceneData(model)

        # =============================================================
        # 第四步：定义物理步进函数和渲染同步函数
        # 将物理更新和渲染同步分离，便于后续扩展控制逻辑
        # =============================================================
        def phys_step():
            model.step(data)

        def render_step():
            render.sync(data)

        # =============================================================
        # 第五步：启动仿真主循环
        # phys_dt: 物理仿真时间步
        # render_fps: 渲染帧率（60fps）
        # run.render_loop 内部处理帧率调度
        # =============================================================
        run.render_loop(
            model.options.timestep,
            60,
            phys_step,
            render_step,
        )


if __name__ == "__main__":
    main()
