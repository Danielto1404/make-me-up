import React, {memo, useMemo} from 'react';


interface LoaderProps {
    size?: number
}

const MjolLoader: React.FC<LoaderProps> = ({
    size = 30
}) => {

    const style = useMemo(() => ({
        width: size,
        height: size
    }), [size])

    return (
        <div className="flex items-center justify-center w-full h-full">
            <div className="lds-roller">
                <div/>
                <div/>
                <div/>
                <div/>
                <div/>
                <div/>
                <div/>
                <div/>
            </div>
        </div>
    )
};

export default memo(MjolLoader);