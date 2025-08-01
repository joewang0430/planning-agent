import { GenerateOutlineResponse, GenerateContentResponse } from "@/data/generateTypes";
import { PageMode } from "@/data/contentTypes";
import React from "react";
import OutlineEditor from "./internals/OutlineEditor";
import PolicyDisplay from "./PolicyDisplay";
import Link from "next/link"; 
import RewriteOutlineBtn from "./buttons/RewriteOutlineBtn";
import DownloadBtn from "./buttons/DownloadBtn";
import WriteContentBtn from "./buttons/WriteContentBtn";
import RewriteContentBtn from "./buttons/RewriteContentBtn";
import FinishPlanningBtn from "./buttons/FinishPlanningBtn";
import ContentEditor from "./internals/ContentEditor";

interface LeftContentProps {
    loading: boolean;
    data: GenerateOutlineResponse | null;
    pageMode: PageMode;
    setPageMode: (mode: PageMode) => void;
    onGenerateContent: () => void; 
    fullContent: GenerateContentResponse | null; 
    onRewriteOutline: () => void;
    isRewriting: boolean;
    onRewriteContent: () => void;
    isRewritingContent: boolean;
};

const LeftContent = ({
    loading, 
    data, 
    pageMode, 
    setPageMode, 
    onGenerateContent, 
    fullContent,
    onRewriteOutline, 
    isRewriting,
    onRewriteContent,
    isRewritingContent,
}: LeftContentProps) => {

    return (
        <div className="flex flex-col h-full min-h-0">
            {/* Policy Display Section */}
            {data && data.policy && <PolicyDisplay policy={data.policy} kb_list={data.kb_list} />}

            {/* middle rollable */}
            <div className="flex-1 min-h-0 overflow-y-auto py-2">
                <div className="space-y-6">
                    {loading ? (
                        <div className="text-center text-gray-500">正在生成...</div>
                    ) : data ? (
                        pageMode === 'outline' ? (
                            <OutlineEditor initialData={data} />
                        ) : (
                            fullContent && data && (
                                <ContentEditor 
                                    initialContentData={fullContent.content}
                                    planTitle={data.title}
                                    policyContext={data.policy}
                                />
                            )
                        )
                    ) : (
                        <div className="text-center text-gray-400">请先在首页输入标题以生成大纲</div>
                    )}
                </div>
            </div>
            {/* button */}
            <div className="mt-auto flex flex-wrap gap-2 justify-between items-center pt-4">
                {pageMode === 'outline' ? (
                    <>
                        <RewriteOutlineBtn 
                            onClick={onRewriteOutline}
                            isLoading={isRewriting}
                        />
                        <div className="flex flex-wrap gap-2">
                            <WriteContentBtn onClick={onGenerateContent}/>
                            <DownloadBtn />
                        </div>
                    </>
                ) : (
                    <>
                        <RewriteContentBtn 
                            onClick={onRewriteContent}
                            isLoading={isRewritingContent}
                            disabled={!fullContent}
                        />
                        <div className="flex flex-wrap gap-2">
                            <FinishPlanningBtn />
                            <DownloadBtn />
                        </div>
                    </>
                )}
                
            </div>
        </div>
    );
};

export default LeftContent;