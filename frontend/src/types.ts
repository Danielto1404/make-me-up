import React from "react";

export interface MediaInput {
    file?: File
    url: string
}

export interface PromptInput {
    prompt: string
}

export interface GenerateFormProps {
    media: MediaInput
    prompts: PromptInput[]
}


export type ReactInputProps = React.DetailedHTMLProps<React.InputHTMLAttributes<HTMLInputElement>, HTMLInputElement>
export type NoRefInputProps = Omit<ReactInputProps, 'ref'>