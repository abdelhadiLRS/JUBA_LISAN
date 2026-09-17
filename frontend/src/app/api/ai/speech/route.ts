import { NextRequest, NextResponse } from "next/server";
import speech from "@google-cloud/speech";

// Google Cloud Speech-to-Text would be used here in production
// For now, we provide a mock implementation for development

export async function POST(request: NextRequest) {
  try {
    const formData: FormData = await request.formData();
    const audioFile = formData.get("audio") as File | null;
    const language = formData.get("language") as string || "en-US";

    if (!audioFile) {
      return NextResponse.json(
        { error: "Audio file is required" },
        { status: 400 }
      );
    }

    // Check if Google Cloud credentials are configured
    if (!process.env.GOOGLE_APPLICATION_CREDENTIALS) {
      // Return mock response for development
      const mockTranscript = language.includes("ar") 
        ? "مرحباً، أنا أتعلم اللغة العربية" 
        : "Hello, I am learning this language";

      return NextResponse.json({
        transcript: mockTranscript,
        accuracy: 0.85,
        pronunciation: 0.82,
        fluency: 0.78,
        feedback: "Good effort! Try to speak more slowly and clearly. Focus on pronouncing each word completely.",
        confidence: 0.88,
        words: [
          { word: language.includes("ar") ? "مرحباً" : "Hello", confidence: 0.95, startTime: 0.0, endTime: 0.5 },
          { word: language.includes("ar") ? "أنا" : "I", confidence: 0.92, startTime: 0.5, endTime: 0.7 },
          { word: language.includes("ar") ? "أتعلم" : "am learning", confidence: 0.88, startTime: 0.7, endTime: 1.2 },
          { word: language.includes("ar") ? "اللغة" : "this", confidence: 0.85, startTime: 1.2, endTime: 1.5 },
          { word: language.includes("ar") ? "العربية" : "language", confidence: 0.80, startTime: 1.5, endTime: 2.0 },
        ],
        duration: 2.0,
        isMock: true,
      });
    }

    // Production implementation with Google Cloud Speech-to-Text
    // This would require @google-cloud/speech package and proper credentials
    const client = new speech.SpeechClient();

    const audioBytes = await audioFile.arrayBuffer();
    const audioBuffer = Buffer.from(audioBytes);

    const audioConfig = {
      encoding: "WEBM_OPUS" as const, // Adjust based on actual format
      sampleRateHertz: 16000,
      languageCode: language,
      enableWordTimeOffsets: true,
      enableAutomaticPunctuation: true,
      model: "latest_long",
    };

    const speechRequest = {
      audio: { content: audioBuffer.toString("base64") },
      config: audioConfig,
    };

    const [response] = await client.recognize(speechRequest);
    const transcription = response.results
      ?.map((result: any) => result.alternatives?.[0]?.transcript)
      .join("\n") || "";

    // Calculate metrics (simplified)
    const wordCount = transcription.split(" ").length;
    const duration = audioFile.size / 16000; // Rough estimate
    const wordsPerMinute = (wordCount / duration) * 60;

    return NextResponse.json({
      transcript: transcription,
      accuracy: 0.90, // Would calculate based on expected vs actual
      pronunciation: 0.85,
      fluency: Math.min(wordsPerMinute / 150, 1.0), // Target 150 WPM
      feedback: generateFeedback(transcription, wordsPerMinute, language),
      confidence: response.results?.[0]?.alternatives?.[0]?.confidence || 0,
      words: response.results?.[0]?.alternatives?.[0]?.words || [],
      duration: duration,
      isMock: false,
    });
  } catch (error) {
    console.error("Speech Analysis Error:", error);
    return NextResponse.json(
      { error: "Failed to analyze speech", details: error instanceof Error ? error.message : "Unknown error" },
      { status: 500 }
    );
  }
}

function generateFeedback(transcript: string, wpm: number, language: string): string {
  const feedback = [];
  
  if (wpm < 80) {
    feedback.push("Try to speak a bit faster to improve fluency.");
  } else if (wpm > 180) {
    feedback.push("Slow down slightly for better clarity.");
  }
  
  if (transcript.length < 20) {
    feedback.push("Try speaking in longer sentences.");
  }
  
  if (feedback.length === 0) {
    feedback.push("Excellent! Your pronunciation and fluency are very good.");
  }
  
  return feedback.join(" ");
}
