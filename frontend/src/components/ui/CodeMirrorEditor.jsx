import { useMemo } from 'react'
import CodeMirror from '@uiw/react-codemirror'
import { EditorView } from '@codemirror/view'
import { EditorState } from '@codemirror/state'
import { HighlightStyle, indentUnit, syntaxHighlighting } from '@codemirror/language'
import { tags as t } from '@lezer/highlight'
import { cpp } from '@codemirror/lang-cpp'
import { python } from '@codemirror/lang-python'

const theme = EditorView.theme({
  '&': {
    color: '#e4e4ea',
    backgroundColor: '#0e0e11',
    fontSize: '13.5px',
  },
  '&.cm-focused': { outline: 'none' },
  '.cm-scroller': { fontFamily: '"JetBrains Mono", ui-monospace, monospace', lineHeight: '1.65', fontVariantLigatures: 'none' },
  '.cm-content': { caretColor: '#f5f5f7', padding: '14px 0' },
  '.cm-line': { padding: '0 16px 0 10px' },
  '.cm-cursor, .cm-dropCursor': { borderLeftColor: '#f5f5f7', borderLeftWidth: '2px' },
  '&.cm-focused > .cm-scroller > .cm-selectionLayer .cm-selectionBackground, .cm-selectionBackground, .cm-content ::selection': {
    backgroundColor: 'rgba(86,186,255,0.24)',
  },
  '.cm-activeLine': { backgroundColor: 'rgba(255,255,255,0.03)' },
  '.cm-gutters': { backgroundColor: '#0e0e11', color: '#4a4a52', border: 'none', paddingLeft: '6px' },
  '.cm-activeLineGutter': { backgroundColor: 'transparent', color: '#c8c8d0' },
  '.cm-lineNumbers .cm-gutterElement': { padding: '0 8px 0 6px', minWidth: '28px' },
  '.cm-matchingBracket, .cm-nonmatchingBracket': { backgroundColor: 'rgba(143,227,160,0.16)', outline: 'none' },
  '.cm-placeholder': { color: '#5d5d66' },
}, { dark: true })

const highlight = HighlightStyle.define([
  { tag: [t.keyword, t.controlKeyword, t.modifier, t.operatorKeyword], color: '#f27aa2' },
  { tag: [t.processingInstruction, t.meta], color: '#f27aa2' },
  { tag: [t.string, t.special(t.string), t.character], color: '#8fe3a0' },
  { tag: [t.number, t.bool, t.null, t.atom], color: '#f6d66f' },
  { tag: [t.comment, t.lineComment, t.blockComment], color: '#6b6b75', fontStyle: 'italic' },
  { tag: [t.function(t.variableName), t.function(t.propertyName), t.macroName], color: '#7de3e8' },
  { tag: [t.typeName, t.className, t.standard(t.typeName)], color: '#7de3e8' },
  { tag: [t.definition(t.variableName)], color: '#f5f5f7' },
  { tag: [t.operator, t.punctuation, t.bracket], color: '#a8a8b3' },
  { tag: t.escape, color: '#f6d66f' },
])

const LANG = { c: cpp, cpp, python }

export default function CodeMirrorEditor({
  value, onChange, language = 'c', readOnly = false, height, minHeight = '240px', maxHeight, label, maxLength, placeholder,
}) {
  const extensions = useMemo(() => [
    (LANG[language] || cpp)(),
    theme,
    syntaxHighlighting(highlight),
    indentUnit.of('    '),
    EditorState.tabSize.of(4),
    EditorView.contentAttributes.of({ 'aria-label': label || 'Code editor' }),
  ], [language, label])

  const handleChange = next => {
    if (!onChange) return
    onChange(maxLength && next.length > maxLength ? next.slice(0, maxLength) : next)
  }

  return (
    <CodeMirror
      value={value}
      onChange={handleChange}
      extensions={extensions}
      theme="none"
      editable={!readOnly}
      readOnly={readOnly}
      height={height}
      minHeight={minHeight}
      maxHeight={maxHeight}
      placeholder={placeholder}
      indentWithTab
      basicSetup={{
        lineNumbers: true,
        foldGutter: false,
        highlightActiveLine: !readOnly,
        highlightActiveLineGutter: !readOnly,
        autocompletion: false,
        closeBrackets: true,
        bracketMatching: true,
        indentOnInput: true,
        searchKeymap: false,
        tabSize: 4,
      }}
    />
  )
}
