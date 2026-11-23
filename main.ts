// "The Typo Fix" — entrypoint Meme Sprint 3: AI Agent Goes Rogue.
// Skrip ini memindahkan entry.png yang sudah dirakit compose.py ke folder
// keluaran yang diminta make.fun, sambil memastikan berkasnya utuh dan
// memenuhi gate (PNG, 1024x1024, maksimal 1 MiB). Node 22, pustaka bawaan
// saja; tanpa jaringan, tanpa jam, tanpa acak — hasilnya deterministik.

import { createHash } from "node:crypto";
import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// Syarat gate dari RULES.txt: PNG utuh, 1024x1024, paling besar 1 MiB.
const TANDA_AWAL_PNG = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);
const BATAS_UKURAN = 1024 * 1024;
const LEBAR_GAMBAR = 1024;
const TINGGI_GAMBAR = 1024;
const NAMA_BERKAS = "entry.png";

const folderRepo = dirname(fileURLToPath(import.meta.url));
const berkasAsal = join(folderRepo, NAMA_BERKAS);

function berhenti(keterangan: string): never {
  console.error(`[typo-fix] gagal: ${keterangan}`);
  process.exit(1);
}

function sidikJari(isi: Buffer): string {
  return createHash("sha256").update(isi).digest("hex");
}

// Tabel CRC-32 (polinomial terbalik 0xedb88320) untuk memeriksa tiap chunk.
const TABEL_CRC32: Uint32Array = (() => {
  const tabel = new Uint32Array(256);
  for (let i = 0; i < 256; i += 1) {
    let c = i;
    for (let k = 0; k < 8; k += 1) {
      c = c % 2 === 0 ? c >>> 1 : 0xedb88320 ^ (c >>> 1);
    }
    tabel[i] = c >>> 0;
  }
  return tabel;
})();

function crc32(isi: Buffer): number {
  let c = 0xffffffff;
  for (const byte of isi) {
    c = TABEL_CRC32[(c ^ byte) & 0xff] ^ (c >>> 8);
  }
  return (c ^ 0xffffffff) >>> 0;
}

// Telusuri semua chunk PNG dan pastikan CRC tiap chunk cocok; chunk pertama
// harus IHDR dan chunk terakhir harus IEND.
function periksaChunk(isi: Buffer): void {
  let posisi = 8;
  let pertama = true;
  let ketemuIend = false;
  while (posisi + 12 <= isi.length) {
    const panjang = isi.readUInt32BE(posisi);
    const tipe = isi.subarray(posisi + 4, posisi + 8).toString("ascii");
    const akhirData = posisi + 8 + panjang;
    if (akhirData + 4 > isi.length) {
      berhenti(`chunk ${tipe} terpotong di offset ${posisi}`);
    }
    const crcTersimpan = isi.readUInt32BE(akhirData);
    const crcHitung = crc32(isi.subarray(posisi + 4, akhirData));
    if (crcHitung !== crcTersimpan) {
      berhenti(`CRC chunk ${tipe} tidak cocok di offset ${posisi}`);
    }
    if (pertama && tipe !== "IHDR") {
      berhenti(`chunk pertama adalah ${tipe}, bukan IHDR`);
    }
    pertama = false;
    if (tipe === "IEND") {
      ketemuIend = true;
      if (akhirData + 4 !== isi.length) {
        berhenti("ada byte sisa setelah chunk IEND");
      }
      break;
    }
    posisi = akhirData + 4;
  }
  if (!ketemuIend) {
    berhenti("chunk IEND tidak ditemukan");
  }
}

function tentukanKeluaran(): string {
  const dariLingkungan = (process.env.MAKEFUN_OUTPUT_DIR ?? "").trim();
  if (dariLingkungan.length > 0) {
    return resolve(dariLingkungan);
  }
  return resolve(folderRepo, "out");
}

// Baca chunk IHDR (lebar di byte 16..19, tinggi di 20..23, big-endian).
function bacaDimensi(isi: Buffer): { lebar: number; tinggi: number } {
  if (isi.length < 24) {
    berhenti("berkas terlalu pendek untuk memuat header PNG");
  }
  return { lebar: isi.readUInt32BE(16), tinggi: isi.readUInt32BE(20) };
}

function periksaGambar(isi: Buffer): string {
  if (isi.length > BATAS_UKURAN) {
    berhenti(
      `${NAMA_BERKAS} berukuran ${isi.length} byte, melewati batas ${BATAS_UKURAN}`,
    );
  }
  if (isi.length < TANDA_AWAL_PNG.length) {
    berhenti(`${NAMA_BERKAS} terlalu pendek untuk menjadi PNG`);
  }
  if (!isi.subarray(0, TANDA_AWAL_PNG.length).equals(TANDA_AWAL_PNG)) {
    berhenti(`${NAMA_BERKAS} tidak diawali signature PNG yang benar`);
  }
  const { lebar, tinggi } = bacaDimensi(isi);
  if (lebar !== LEBAR_GAMBAR || tinggi !== TINGGI_GAMBAR) {
    berhenti(
      `dimensi ${lebar}x${tinggi}, padahal gate meminta ${LEBAR_GAMBAR}x${TINGGI_GAMBAR}`,
    );
  }
  periksaChunk(isi);
  return sidikJari(isi);
}

function utama(): void {
  if (!existsSync(berkasAsal)) {
    berhenti(`berkas sumber tidak ada: ${berkasAsal}`);
  }
  const isiAsal = readFileSync(berkasAsal);
  const sidikAsal = periksaGambar(isiAsal);

  const folderKeluaran = tentukanKeluaran();
  mkdirSync(folderKeluaran, { recursive: true });
  const berkasTujuan = join(folderKeluaran, NAMA_BERKAS);
  copyFileSync(berkasAsal, berkasTujuan);

  // Verifikasi ulang dari hasil salinan: hash dan isi byte harus sama.
  const isiSalinan = readFileSync(berkasTujuan);
  const sidikSalinan = sidikJari(isiSalinan);
  if (sidikSalinan !== sidikAsal) {
    berhenti(
      `salinan tidak identik: ${sidikSalinan} berbeda dari ${sidikAsal}`,
    );
  }
  if (!isiSalinan.equals(isiAsal)) {
    berhenti("isi byte salinan berbeda dari sumber");
  }
  console.log(
    `[typo-fix] OK ${berkasTujuan} — ${isiSalinan.length} byte, sha256 ${sidikSalinan}`,
  );
}

utama();
