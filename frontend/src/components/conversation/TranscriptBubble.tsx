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
      <div className="relative mb-0 flex-shrink-0">
        <span
          className={`pointer-events-none absolute inset-[-4px] rounded-full border transition-[border-color,opacity] duration-700 ${
            speaking
              ? 'border-[color-mix(in_srgb,var(--duo-green)_65%,transparent)] animate-halo-speaking'
              : 'border-[color-mix(in_srgb,var(--duo-green)_15%,transparent)] animate-halo-idle'
          }`}
        />
        <div className="h-[30px] w-[30px] overflow-hidden rounded-full border border-[var(--duo-line)] bg-[color-mix(in_srgb,var(--duo-green)_12%,transparent)] shadow-sm">
          {!isUser ? (
            <Image
              src="/logo_head.png"
              alt="Tutor"
              width={30}
              height={30}
              className="h-full w-full object-cover"
            />
          ) : userAvatar ? (
            <AuthAvatarImage
              avatar={userAvatar}
              alt=""
              width={32}
              height={32}
              className="h-full w-full object-cover"
              fallback={
                <div className="flex h-full w-full items-center justify-center bg-[color-mix(in_srgb,var(--duo-green)_12%,transparent)]">
                  <span className="select-none font-sans font-bold text-[var(--duo-green-dark)]">
                    {(userInitial ?? '?').toUpperCase()}
                  </span>
                </div>
              }
            />
          ) : (
            <div className="bg-[color-mix(in_srgb,var(--duo-green)_8%,transparent)] flex h-full w-full items-center justify-center">
              <span className="text-[var(--duo-muted)] font-sans select-none">
                {(userInitial ?? '?').toUpperCase()}
              </span>
            </div>
          )}
        </div>
      </div>

      <div
        className={`flex max-w-[80%] flex-col gap-0.5 sm:max-w-[70%] ${isUser ? 'items-end' : 'items-start'}`}
      >
        <span className="text-[var(--duo-muted)] font-sans text-[10px] font-bold tracking-wide uppercase">
          {isUser ? t('you') : t('assistant')}
        </span>
        <TargetLanguageText
          as="div"
          languageCode={languageCode}
          className={`rounded-[10px] border px-3 py-2 leading-relaxed break-words shadow-sm ${
            isUser
              ? 'bg-[var(--duo-green)] text-white border-[var(--duo-green-dark)]'
              : 'bg-[var(--duo-card)] text-[var(--duo-ink)] border-[var(--duo-line)]'
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
