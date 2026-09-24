import Image from 'next/image'
import { useTranslations } from 'next-intl'
import { TargetLanguageText } from '@/components/TargetLanguageText'
import { AuthAvatarImage } from '@/components/AuthAvatarImage'

interface Props {
  role: 'user' | 'assistant'
  text: string
  streaming?: boolean
  speaking?: boolean
  userAvatar?: string | null
  userInitial?: string
  languageCode?: string | null
}

export default function TranscriptBubble({
  role,
  text,
  streaming = false,
  speaking = false,
  userAvatar,
  userInitial,
  languageCode,
}: Props) {
  const t = useTranslations('conversation')
  const isUser = role === 'user'

  return (
    <div
      className={`flex items-end gap-2 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}
    >
      {/* Avatar */}
      <div className="relative mb-0.5 flex-shrink-0">
        <span
          className={`pointer-events-none absolute inset-[-5px] rounded-full border-2 transition-[border-color,opacity] duration-700 ${
            speaking
              ? 'border-[color-mix(in_srgb,var(--juba-app-green)_65%,transparent)] animate-halo-speaking'
              : 'border-[color-mix(in_srgb,var(--juba-app-green)_15%,transparent)] animate-halo-idle'
          }`}
        />
        <div className="border-[var(--juba-app-line)] h-7 w-7 overflow-hidden rounded-full border">
          {!isUser ? (
            <Image
              src="/logo_head.png"
              alt="Tutor"
              width={28}
              height={28}
              className="h-full w-full object-cover"
            />
          ) : userAvatar ? (
            <AuthAvatarImage
              avatar={userAvatar}
              alt=""
              width={28}
              height={28}
              className="h-full w-full object-cover"
              fallback={
                <div className="bg-[#f3f7ef] flex h-full w-full items-center justify-center">
                  <span className="text-[var(--juba-app-muted)] font-mono select-none">
                    {(userInitial ?? '?').toUpperCase()}
                  </span>
                </div>
              }
            />
          ) : (
            <div className="bg-[#f3f7ef] flex h-full w-full items-center justify-center">
              <span className="text-[var(--juba-app-muted)] font-mono select-none">
                {(userInitial ?? '?').toUpperCase()}
              </span>
            </div>
          )}
        </div>
      </div>

      <div
        className={`flex max-w-[75%] flex-col gap-1 ${isUser ? 'items-end' : 'items-start'}`}
      >
        <span className="text-[var(--juba-app-muted)] font-mono tracking-widest uppercase">
          {isUser ? t('you') : t('assistant')}
        </span>
        <TargetLanguageText
          as="div"
          languageCode={languageCode}
          className={`border px-4 py-3 ${
            isUser
              ? 'bg-[var(--juba-app-green)] text-white border-[var(--juba-app-green-dark)]'
              : 'bg-[var(--juba-app-surface)] text-[var(--juba-app-ink)] border-[var(--juba-app-line)]'
          }`}
        >
          {text}
          {streaming && (
            <span className="ml-1 inline-block h-3 w-1 animate-pulse bg-current align-middle" />
          )}
        </TargetLanguageText>
      </div>
    </div>
  )
}
