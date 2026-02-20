/* BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated. */
/* KR-018: Kalibrasyon gereksinimi için görüntü metadata'sı görünür tutulur. */

import { useMemo, useState } from "react";

export interface ViewerImage {
  readonly id: string;
  readonly src: string;
  readonly alt: string;
  readonly spectralBand: "RGB" | "NDVI" | "NIR" | "THERMAL";
  readonly calibrated: boolean;
}

export interface ImageViewerProps {
  readonly images: readonly ViewerImage[];
  readonly initialImageId?: string;
  readonly corrId?: string;
  readonly requestId?: string;
}

const ZOOM_STEP = 0.25;

export function ImageViewer({ images, initialImageId, corrId, requestId }: ImageViewerProps) {
  const [zoom, setZoom] = useState(1);
  const [activeId, setActiveId] = useState(initialImageId ?? images[0]?.id);

  const activeImage = useMemo(
    () => images.find((image) => image.id === activeId) ?? images[0],
    [activeId, images]
  );

  if (!activeImage) {
    return <p role="status">Gösterilecek görüntü bulunamadı.</p>;
  }

  return (
    <section aria-label="Görüntü inceleyici" data-corr-id={corrId} data-request-id={requestId}>
      <div className="mb-3 flex items-center gap-2">
        <button type="button" onClick={() => setZoom((prev) => Math.max(1, prev - ZOOM_STEP))}>
          Yakınlaştır -
        </button>
        <button type="button" onClick={() => setZoom((prev) => Math.min(3, prev + ZOOM_STEP))}>
          Yakınlaştır +
        </button>
        <output aria-live="polite">%{Math.round(zoom * 100)}</output>
      </div>

      <figure>
        <img
          src={activeImage.src}
          alt={activeImage.alt}
          style={{ transform: `scale(${zoom})`, transformOrigin: "center", maxWidth: "100%" }}
        />
        <figcaption>
          Bant: {activeImage.spectralBand} · Kalibrasyon: {activeImage.calibrated ? "Hazır" : "Eksik"}
        </figcaption>
      </figure>

      <ul className="mt-4 flex flex-wrap gap-2" aria-label="Görüntü listesi">
        {images.map((image) => (
          <li key={image.id}>
            <button
              type="button"
              onClick={() => setActiveId(image.id)}
              aria-pressed={activeId === image.id}
              className="rounded border px-2 py-1"
            >
              {image.spectralBand}
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}
