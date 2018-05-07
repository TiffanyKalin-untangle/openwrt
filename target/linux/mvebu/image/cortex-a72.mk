ifeq ($(SUBTARGET),cortexa72)

define Device/marvell_macchiatobin
  $(call Device/Default-arm64)
  DEVICE_TITLE := MACCHIATObin (SolidRun Armada 8040 Community Board)
  DEVICE_PACKAGES += kmod-i2c-core kmod-i2c-mux kmod-i2c-mux-pca954x
  DEVICE_DTS := armada-8040-mcbin
  SUPPORTED_DEVICES := marvell,armada8040-mcbin
endef
TARGET_DEVICES += marvell_macchiatobin

define Device/marvell_armada8040-db
  $(call Device/Default-arm64)
  DEVICE_TITLE := Marvell Armada 8040 DB board
  DEVICE_DTS := armada-8040-db
  IMAGE/sdcard.img.gz := boot-img-ext4 | sdcard-img-ext4 | gzip | append-metadata
endef
TARGET_DEVICES += marvell_armada8040-db

define Device/marvell_armada7040-db
  $(call Device/Default-arm64)
  DEVICE_TITLE := Marvell Armada 7040 DB board
  DEVICE_DTS := armada-7040-db
  IMAGE/sdcard.img.gz := boot-img-ext4 | sdcard-img-ext4 | gzip | append-metadata
endef
TARGET_DEVICES += marvell_armada7040-db

define Device/armada-8040-db
  KERNEL_NAME := Image
  KERNEL := kernel-bin
  DEVICE_TITLE := Marvell Armada 8040 DB board
  DEVICE_PACKAGES := e2fsprogs ethtool mkf2fs kmod-fs-vfat kmod-mmc
  IMAGES := sdcard.img.gz
  IMAGE/sdcard.img.gz := boot-img-ext4 | sdcard-img-ext4 | gzip | append-metadata
  DEVICE_DTS := armada-8040-db
  DTS_DIR := $(DTS_DIR)/marvell
  SUPPORTED_DEVICES := marvell,armada8040-db
endef
TARGET_DEVICES += armada-8040-db

define Device/armada-7040-db
  KERNEL_NAME := Image
  KERNEL := kernel-bin
  DEVICE_TITLE := Marvell Armada 7040 DB board
  DEVICE_PACKAGES := e2fsprogs ethtool mkf2fs kmod-fs-vfat kmod-mmc
  IMAGES := sdcard.img.gz
  IMAGE/sdcard.img.gz := boot-img-ext4 | sdcard-img-ext4 | gzip | append-metadata
  DEVICE_DTS := armada-7040-db
  DTS_DIR := $(DTS_DIR)/marvell
  SUPPORTED_DEVICES := marvell,armada7040-db
endef
TARGET_DEVICES += armada-7040-db

endif
