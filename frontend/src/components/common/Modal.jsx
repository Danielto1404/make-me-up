import React, {useEffect, useRef} from 'react'
import {AiOutlineCloseCircle} from 'react-icons/ai'

const Modal = ({
    close = () => {
    },
    closeOnBgClick = true,
    closeOnEscape = true,
    children,
    className = "fixed inset-0 z-[150] flex items-center justify-center p-4",
    style = {
        backgroundColor: `rgba(0, 0, 0, 0.9)`
    },
}) => {
    const modalRef = useRef(null)

    useEffect(() => {
        const onKeydown = (event) => {
            if (event.key === 'Escape') {
                close()
            }
        }

        if (closeOnEscape) {
            document.addEventListener('keydown', onKeydown)
        }

        return () => {
            document.removeEventListener('keydown', onKeydown)
        }
    }, [close, closeOnEscape])

    const _bgClick = (event) => {
        if (closeOnBgClick && event.target === modalRef.current) {
            close()
        }
    }

    return (<div
        ref={modalRef}
        onClick={_bgClick}
        className={className}
        style={style}
    >
        <div className="relative">
            <button onClick={close}>
                <AiOutlineCloseCircle className="bg-black fill-white rounded-full absolute top-3 -right-3 w-8 h-8"/>
            </button>
            {children}
        </div>
    </div>)
}

export default Modal