import React from 'react';
import {useFieldArray, useFormContext} from "react-hook-form";
import BaseInput from "./BaseInput";
import MinusButton from "../buttons/MinusButton";
import {PromptInput} from "../../../types";
import PlusButton from "../buttons/PlusButton";
import InputLabel from "./InputLabel";

const PromptsInput = () => {

    const {control, formState} = useFormContext<{ prompts: PromptInput[] }>()

    const {fields, append, remove} = useFieldArray({
        control,
        name: "prompts"
    });

    return (
        <div>
            <InputLabel label="Text criteria"
                        description="You can add text prompt related to make which you want to fit. Maximum 2 criteria."
            />
            {fields.map((field, index) =>
                <div key={field.id}
                     className="grid grid-cols-[45px_1fr] items-start gap-4 my-3">
                    <MinusButton onClick={() => remove(index)}/>
                    <BaseInput placeholder="red lips"
                               error={formState?.errors?.prompts?.[index].prompt?.message}
                               {...control.register(`prompts.${index}.prompt`, {
                                   maxLength: {
                                       value: 20,
                                       message: "Maximum length for one criteria is 20 symbols"
                                   }
                               })}
                    />
                </div>
            )}
            {fields.length < 2
                &&
                <div className="w-[45px] h-[45px]">
                    <PlusButton onClick={() => append({prompt: ""})}/>
                </div>
            }
        </div>
    );
};

export default PromptsInput;