import { useState } from 'react'
import RichText from '../../learning/RichText'
import CodeArea from '../../learning/CodeArea'
import { CODE_CAP, ItemActions } from './shared'

export default function WriteCodeView({ item, onSubmit, disabled }) {
  const [code, setCode] = useState(item.body.starter_code || '')

  return (
    <div>
      <RichText text={item.body.statement} className="text-white/85 text-[15px] mb-4" />
      <CodeArea value={code} onChange={setCode} disabled={disabled} maxLength={CODE_CAP}
        label="Your code" />
      <ItemActions canSubmit={!!code.trim()} disabled={disabled}
        onSubmit={() => onSubmit({ code })} onSkip={() => onSubmit({ code: '' })} />
    </div>
  )
}
