local Bloom = PostProcessing.bloom
local colorGrading = PostProcessing.colorGrading

Bloom.enableEffect({"intensity", "diffusion"})
Bloom.intensity = Channel.keyframe().addKey(-10000, 20)
Bloom.diffusion = Channel.keyframe().addKey(-10000, 5)

colorGrading.enableEffect({"lift", "gamma", "gain"})
colorGrading.liftX = Channel.keyframe().addKey(-10000, -0.5)
colorGrading.liftY = Channel.keyframe().addKey(-10000, -0.5)
colorGrading.liftZ = Channel.keyframe().addKey(-10000, -0.5)
colorGrading.gainX = Channel.keyframe().addKey(-10000, 2)
colorGrading.gainY = Channel.keyframe().addKey(-10000, 2)
colorGrading.gainZ = Channel.keyframe().addKey(-10000, 2)
