{
    "name": "KSI Service Center & Warranty Management",
    "version": "17.0.1.0.0",
    "category": "Services/Hardware",
    "summary": "Manajemen Servis Perangkat & Klaim Garansi Hardware (Partner Axioo)",
    "description": """
Modul Kustom untuk Pengelolaan Service Center Hardware:
- Registrasi Master Perangkat / Laptop
- Manajemen Tiket Servis (Penerimaan, Diagnosa, Selesai, Diambil)
- Pengecekan Masa Garansi Otomatis
- Penggunaan & Rekapitulasi Suku Cadang (Spare Parts)
- Perhitungan Total Biaya Servis
    """,
    "author": "Hafizh Irfansyah",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "data/service_sequence.xml",
        "views/service_device_views.xml",
        "views/service_ticket_views.xml",
        "views/service_menus.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
