# Pic2ID - AI Passport Photo Generator

Welcome to Pic2ID! This is a simple and intelligent web app that transforms any portrait photo into a professional passport-style photo, complete with background removal and a smart suit & tie overlay. No studio visits required—make your official ID photos right at home.

## What Pic2ID Does

- Upload a portrait image in JPG or PNG format
- Automatically remove the background while preserving your face
- Overlay a formal suit and tie aligned perfectly with your photo
- Crop and resize the output to standard passport dimensions (600x600 pixels)
- Download your ready-to-print passport photo instantly

## Why Use Pic2ID?

Because who wants to book expensive photo sessions or wrestle with complicated image editors? Pic2ID lets you create high-quality, compliant passport photos with just a few clicks.

## How it Works (Behind the Scenes)

- Uses AI-powered background removal to cleanly isolate the subject
- Detects your face to ensure the suit overlay fits perfectly without hiding you
- Handles image cropping and resizing to official passport photo standards
- All processing happens within the app—your photos stay with you

## Getting Started

Simply run the Streamlit app, upload your portrait, then follow the buttons in order:
1. Remove Background
2. Add Suit & Tie
3. Format as Passport Photo
4. Download your polished ID photo

## Tech Stack

- Python with Streamlit for the interactive UI
- `rembg` for background removal
- OpenCV and face detection for precise overlay positioning
- Pillow for image processing and compositing

## Improvements & Next Steps

- Add options for different country-specific passport photo sizes
- Support multiple suit styles or colors
- Enhance the background replacement with custom solid colors

## Feedback & Contributions

Bug reports, feature requests, or ideas? Pull requests are welcome! Help us make passport photo creation painless and fun.
