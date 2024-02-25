const express = require('express');
const multer = require('multer');
const { exec } = require('child_process');

const app = express();
const port = 3000;

// Configure multer for handling file uploads
const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

// Serve the HTML file
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

// Handle video upload and conversion
app.post('/upload', upload.single('video'), (req, res) => {
    const videoBuffer = req.file.buffer;

    // Convert the uploaded video to MP4 using FFmpeg
    const command = `ffmpeg -i pipe:0 -c:v libx264 -c:a aac -strict experimental -movflags +faststart output.mp4`;

    const ffmpegProcess = exec(command, (error, stdout, stderr) => {
        if (error) {
            console.error(`FFmpeg error: ${error}`);
            res.status(500).json({ error: 'Internal Server Error' });
            return;
        }

        console.log('Video conversion successful');
        res.status(200).json({ message: 'Video uploaded and converted successfully' });
    });

    ffmpegProcess.stdin.write(videoBuffer);
    ffmpegProcess.stdin.end();
});

app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
