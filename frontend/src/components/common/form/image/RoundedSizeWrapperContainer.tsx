import React from 'react';

const RoundedSizeWrapperContainer: React.FC<{ classes?: string }> = ({
    classes,
    children
}) => {
    return (
        <div className={classes}>
            {children}
        </div>
    );
};

export default RoundedSizeWrapperContainer;