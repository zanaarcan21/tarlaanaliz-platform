// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
export interface ResultGalleryItem {
  id: string;
  title: string;
  previewUrl: string;
}

interface ResultGalleryProps {
  items: ResultGalleryItem[];
  selectedId?: string;
  onSelect: (id: string) => void;
}

export function ResultGallery({ items, selectedId, onSelect }: ResultGalleryProps) {
  return (
    <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3" data-testid="result-gallery">
      {items.map((item) => {
        const selected = selectedId === item.id;
        return (
          <button
            key={item.id}
            type="button"
            onClick={() => onSelect(item.id)}
            className={`overflow-hidden rounded-lg border text-left transition ${selected ? 'border-emerald-500 ring-1 ring-emerald-400' : 'border-slate-200 hover:border-slate-300'}`}
            data-testid={`result-gallery-item-${item.id}`}
            aria-pressed={selected}
          >
            <img src={item.previewUrl} alt={item.title} className="h-36 w-full object-cover" loading="lazy" />
            <div className="p-2 text-sm font-medium text-slate-900">{item.title}</div>
          </button>
        );
      })}
    </div>
  );
}
