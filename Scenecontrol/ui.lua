local combo = Scene.combo
local composer = Scene.composer
local difficultyBackground = Scene.difficultyBackground
local difficultyText = Scene.difficultyText
local infoPanel = Scene.infoPanel
local jacket = Scene.jacket
local jacketBackground = Scene.jacketBackground
local pauseButton = Scene.pauseButton
local score = Scene.score
local scoreTitle = Scene.scoreTitle
local skyinputlabel = Scene.skyInputLabel
local skyinputline = Scene.skyInputLine
local title = Scene.title
local screenWidth = Context.screenWidth.valueAt(0)
local screenHeight = Context.screenHeight.valueAt(0)
local ratio = screenWidth / screenHeight

skyinputlabel.translationY = Channel.keyframe().addKey(-10000, -1000, "l")
skyinputline.translationY = Channel.keyframe().addKey(-10000, -1000, "l")
infoPanel.colorA = Channel.keyframe().addKey(-10000, 0, "l")

if ratio < 16.1 / 9 and ratio > 15.9 / 9 then
    combo.translationY = Channel.keyframe().addKey(-10000, screenHeight * 0.67, "l")
    combo.scaleX = Channel.keyframe().addKey(-10000, 0.5, "l")
    combo.scaleY = Channel.keyframe().addKey(-10000, 0.5, "l")
    combo.colorR = Channel.keyframe().addKey(-10000, 255, "l")
    combo.colorG = Channel.keyframe().addKey(-10000, 255, "l")
    combo.colorB = Channel.keyframe().addKey(-10000, 255, "l")

    composer.scaleX = Channel.keyframe().addKey(-10000, 1.75, "l")
    composer.scaleY = Channel.keyframe().addKey(-10000, 1.75, "l")
    composer.translationX = Channel.keyframe().addKey(-10000, screenWidth * 0.44, "l")
    composer.translationY = Channel.keyframe().addKey(-10000, -screenHeight * 2.7, "l")

    difficultyBackground.colorA = Channel.keyframe().addKey(-10000, 0, "l")

    difficultyText.scaleX = Channel.keyframe().addKey(-10000, 2, "l")
    difficultyText.scaleY = Channel.keyframe().addKey(-10000, 2, "l")
    difficultyText.translationX = Channel.keyframe().addKey(-10000, -screenWidth * 1.97, "l")
    difficultyText.translationY = Channel.keyframe().addKey(-10000, -screenHeight * 2.17, "l")

    jacket.colorA = Channel.keyframe().addKey(-10000, 0, "l")
    jacketBackground.colorA = Channel.keyframe().addKey(-10000, 0, "l")

    pauseButton.colorA = Channel.keyframe().addKey(-10000, 0, "l")

    score.translationX = Channel.keyframe().addKey(-10000, screenWidth * 0.23, "l")
    score.translationY = Channel.keyframe().addKey(-10000, screenHeight * 0.34, "l")

    scoreTitle.translationX = Channel.keyframe().addKey(-10000, screenWidth * 0.56, "l")
    scoreTitle.translationY = Channel.keyframe().addKey(-10000, screenHeight * 0.19, "l")
    scoreTitle.text = TextChannel.create().addKey(-10000, "score", "l")
    scoreTitle.scaleX = Channel.keyframe().addKey(-10000, 2, "l")
    scoreTitle.scaleY = Channel.keyframe().addKey(-10000, 2, "l")

    title.scaleX = Channel.keyframe().addKey(-10000, 1.5, "l")
    title.scaleY = Channel.keyframe().addKey(-10000, 1.5, "l")
    title.translationX = Channel.keyframe().addKey(-10000, screenWidth * 0.3, "l")
    title.translationY = Channel.keyframe().addKey(-10000, -screenHeight * 2.63, "l")
end

if ratio < 4.1 / 3 and ratio > 3.9 / 3 then
    combo.translationY = Channel.keyframe().addKey(-10000, screenHeight * 0.67, "l")
    combo.scaleX = Channel.keyframe().addKey(-10000, 0.5, "l")
    combo.scaleY = Channel.keyframe().addKey(-10000, 0.5, "l")
    combo.colorR = Channel.keyframe().addKey(-10000, 255, "l")
    combo.colorG = Channel.keyframe().addKey(-10000, 255, "l")
    combo.colorB = Channel.keyframe().addKey(-10000, 255, "l")

    composer.scaleX = Channel.keyframe().addKey(-10000, 1.75, "l")
    composer.scaleY = Channel.keyframe().addKey(-10000, 1.75, "l")
    composer.translationX = Channel.keyframe().addKey(-10000, screenWidth * 0.5, "l")
    composer.translationY = Channel.keyframe().addKey(-10000, -screenHeight * 2.7, "l")

    difficultyBackground.colorA = Channel.keyframe().addKey(-10000, 0, "l")

    difficultyText.scaleX = Channel.keyframe().addKey(-10000, 2, "l")
    difficultyText.scaleY = Channel.keyframe().addKey(-10000, 2, "l")
    difficultyText.translationX = Channel.keyframe().addKey(-10000, -screenWidth * 1.87, "l")
    difficultyText.translationY = Channel.keyframe().addKey(-10000, -screenHeight * 2.17, "l")

    jacket.colorA = Channel.keyframe().addKey(-10000, 0, "l")
    jacketBackground.colorA = Channel.keyframe().addKey(-10000, 0, "l")

    pauseButton.colorA = Channel.keyframe().addKey(-10000, 0, "l")

    score.translationX = Channel.keyframe().addKey(-10000, screenWidth * 0.25, "l")
    score.translationY = Channel.keyframe().addKey(-10000, screenHeight * 0.28, "l")

    scoreTitle.translationX = Channel.keyframe().addKey(-10000, screenWidth * 0.64, "l")
    scoreTitle.translationY = Channel.keyframe().addKey(-10000, screenHeight * 0.15, "l")
    scoreTitle.text = TextChannel.create().addKey(-10000, "score", "l")
    scoreTitle.scaleX = Channel.keyframe().addKey(-10000, 2, "l")
    scoreTitle.scaleY = Channel.keyframe().addKey(-10000, 2, "l")

    title.scaleX = Channel.keyframe().addKey(-10000, 1.5, "l")
    title.scaleY = Channel.keyframe().addKey(-10000, 1.5, "l")
    title.translationX = Channel.keyframe().addKey(-10000, screenWidth * 0.34, "l")
    title.translationY = Channel.keyframe().addKey(-10000, -screenHeight * 2.63, "l")
end
