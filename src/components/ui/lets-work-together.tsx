"use client"

import type React from "react"
import { useState } from "react"
import { ArrowUpRight, Loader2 } from "lucide-react"

interface LetsWorkTogetherProps {
    onAsk: () => void
    answer?: string
    loading?: boolean
}

export function LetsWorkTogether({ onAsk, answer, loading }: LetsWorkTogetherProps) {
    const [isHovered, setIsHovered] = useState(false)
    const [isClicked, setIsClicked] = useState(false)
    const [showSuccess, setShowSuccess] = useState(false)
    const [isButtonHovered, setIsButtonHovered] = useState(false)

    const handleClick = (e: React.MouseEvent<HTMLDivElement>) => {
        e.preventDefault()
        if (loading) return;

        setIsClicked(true)
        onAsk() // Call existing logic

        setTimeout(() => {
            setShowSuccess(true)
        }, 500)
    }


    return (
        <section className="flex flex-col items-center justify-center px-4 py-8 overflow-hidden min-h-[400px]">
            <div className="relative flex flex-col items-center gap-12 w-full max-w-sm">
                <div
                    className="absolute inset-0 z-10 flex flex-col items-center justify-center gap-8 transition-all duration-700 ease-[cubic-bezier(0.16,1,0.3,1)]"
                    style={{
                        opacity: showSuccess ? 1 : 0,
                        transform: showSuccess ? "translateY(0) scale(1)" : "translateY(20px) scale(0.95)",
                        pointerEvents: showSuccess ? "auto" : "none",
                    }}
                >
                    {/* Elegant heading */}
                    <div className="flex flex-col items-center gap-2">
                        <span
                            className="text-[10px] font-medium tracking-[0.3em] uppercase text-muted-foreground transition-all duration-500"
                            style={{
                                transform: showSuccess ? "translateY(0)" : "translateY(10px)",
                                opacity: showSuccess ? 1 : 0,
                                transitionDelay: "100ms",
                            }}
                        >
                            Response
                        </span>
                        <h3
                            className="text-xl font-light tracking-tight text-foreground transition-all duration-500"
                            style={{
                                transform: showSuccess ? "translateY(0)" : "translateY(10px)",
                                opacity: showSuccess ? 1 : 0,
                                transitionDelay: "200ms",
                            }}
                        >
                            Summary
                        </h3>
                    </div>

                    {/* AI Answer Display */}
                    <div
                        className="w-full bg-slate-800/50 p-4 rounded-xl border border-slate-700 text-sm leading-relaxed text-slate-300 transition-all duration-1000"
                        style={{
                            opacity: showSuccess ? 1 : 0,
                            transform: showSuccess ? "translateY(0)" : "translateY(10px)",
                            transitionDelay: "300ms"
                        }}
                    >
                        {answer || (loading ? "Synthesizing answer..." : "Thinking...")}
                    </div>

                    {/* Book a call button (reset action) */}
                    <button
                        onClick={() => { setIsClicked(false); setShowSuccess(false); }}
                        onMouseEnter={() => setIsButtonHovered(true)}
                        onMouseLeave={() => setIsButtonHovered(false)}
                        className="group relative flex items-center gap-4 transition-all duration-500 cursor-pointer"
                        style={{
                            transform: showSuccess
                                ? isButtonHovered
                                    ? "translateY(0) scale(1.02)"
                                    : "translateY(0) scale(1)"
                                : "translateY(15px) scale(1)",
                            opacity: showSuccess ? 1 : 0,
                            transitionDelay: "150ms",
                        }}
                    >
                        <div className="h-px w-6 bg-border opacity-50" />
                        <div
                            className="relative flex items-center gap-3 overflow-hidden rounded-full border px-6 py-2 transition-all duration-500"
                            style={{
                                borderColor: isButtonHovered ? "var(--foreground)" : "var(--border)",
                                backgroundColor: isButtonHovered ? "var(--foreground)" : "transparent",
                            }}
                        >
                            <span className="text-xs font-medium tracking-wide" style={{ color: isButtonHovered ? "var(--background)" : "var(--foreground)" }}>
                                Ask Another
                            </span>
                        </div>
                        <div className="h-px w-6 bg-border opacity-50" />
                    </button>
                </div>

                {/* Available indicator */}
                <div
                    className="flex items-center gap-3 transition-all duration-500"
                    style={{
                        opacity: isClicked ? 0 : 1,
                        transform: isClicked ? "translateY(-20px)" : "translateY(0)",
                        pointerEvents: isClicked ? "none" : "auto",
                    }}
                >
                    <span className="relative flex size-2">
                        <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75" />
                        <span className="relative inline-flex size-2 rounded-full bg-emerald-500" />
                    </span>
                    <span className="text-[10px] font-medium tracking-widest uppercase text-muted-foreground">
                        System Online
                    </span>
                </div>

                {/* The Main Ask Action */}
                <div
                    className="group relative cursor-pointer"
                    onMouseEnter={() => setIsHovered(true)}
                    onMouseLeave={() => setIsHovered(false)}
                    onClick={handleClick}
                    style={{
                        pointerEvents: isClicked ? "none" : "auto",
                    }}
                >
                    <div className="flex flex-col items-center gap-6">
                        <h2
                            className="relative text-center text-4xl font-light tracking-tight text-foreground transition-all duration-700 ease-[cubic-bezier(0.16,1,0.3,1)]"
                            style={{
                                opacity: isClicked ? 0 : 1,
                                transform: isClicked ? "translateY(-40px) scale(0.95)" : "translateY(0) scale(1)",
                            }}
                        >
                            <span className="block overflow-hidden">
                                <span
                                    className="block transition-transform duration-700 ease-[cubic-bezier(0.16,1,0.3,1)]"
                                    style={{
                                        transform: isHovered && !isClicked ? "translateY(-8%)" : "translateY(0)",
                                    }}
                                >
                                    Synthesize
                                </span>
                            </span>
                            <span className="block overflow-hidden">
                                <span
                                    className="block transition-transform duration-700 ease-[cubic-bezier(0.16,1,0.3,1)] delay-75"
                                    style={{
                                        transform: isHovered && !isClicked ? "translateY(-8%)" : "translateY(0)",
                                    }}
                                >
                                    <span className="text-muted-foreground/60">answer</span>
                                </span>
                            </span>
                        </h2>

                        <div className="relative mt-2 flex size-14 items-center justify-center">
                            <div
                                className="pointer-events-none absolute inset-0 rounded-full border transition-all ease-out"
                                style={{
                                    borderColor: isClicked ? "var(--foreground)" : isHovered ? "var(--foreground)" : "var(--border)",
                                    backgroundColor: isClicked ? "transparent" : isHovered ? "var(--foreground)" : "transparent",
                                    transform: isClicked ? "scale(3)" : isHovered ? "scale(1.1)" : "scale(1)",
                                    opacity: isClicked ? 0 : 1,
                                    transitionDuration: isClicked ? "700ms" : "500ms",
                                }}
                            />
                            {loading ? (
                                <Loader2 className="size-5 animate-spin text-foreground" />
                            ) : (
                                <ArrowUpRight
                                    className="size-5 transition-all ease-[cubic-bezier(0.16,1,0.3,1)]"
                                    style={{
                                        transform: isClicked
                                            ? "translate(100px, -100px) scale(0.5)"
                                            : isHovered
                                                ? "translate(2px, -2px)"
                                                : "translate(0, 0)",
                                        opacity: isClicked ? 0 : 1,
                                        color: isHovered && !isClicked ? "var(--background)" : "var(--foreground)",
                                        transitionDuration: isClicked ? "600ms" : "500ms",
                                    }}
                                />
                            )}
                        </div>
                    </div>

                    <div className="absolute -left-8 top-1/2 -translate-y-1/2">
                        <div
                            className="h-px w-6 bg-border transition-all duration-500 opacity-50"
                            style={{
                                transform: isClicked ? "scaleX(0) translateX(-20px)" : isHovered ? "scaleX(1.5)" : "scaleX(1)",
                            }}
                        />
                    </div>
                    <div className="absolute -right-8 top-1/2 -translate-y-1/2">
                        <div
                            className="h-px w-6 bg-border transition-all duration-500 opacity-50"
                            style={{
                                transform: isClicked ? "scaleX(0) translateX(20px)" : isHovered ? "scaleX(1.5)" : "scaleX(1)",
                            }}
                        />
                    </div>
                </div>

                <div
                    className="mt-4 flex flex-col items-center gap-2 text-center transition-all duration-500 delay-100"
                    style={{
                        opacity: isClicked ? 0 : 1,
                        transform: isClicked ? "translateY(20px)" : "translateY(0)",
                        pointerEvents: isClicked ? "none" : "auto",
                    }}
                >
                    <p className="max-w-[240px] text-[10px] leading-relaxed text-muted-foreground italic">
                        "Ask what's on your mind. Let's decode the knowledge together."
                    </p>
                </div>
            </div>
        </section>
    )
}
