# Manga109 Dataset: Comprehensive Statistics Summary

**Date:** 2025-11-04  
**Total Images:** 10,619

---

## 📊 1. Overview

| Category | Total Annotations | Images with Category | Coverage |
|----------|------------------|---------------------|----------|
| **Balloon** | 130,180 | 9,916 | 93.4% |
| **Body (Character)** | 157,152 | 10,071 | 94.8% |
| **Onomatopeia** | 60,549 | 8,396 | 79.1% |

---

## 🔢 2. Count Statistics (per image)

*For images containing each category*

| Metric | Balloon | Body | Onomatopeia |
|--------|---------|------|-------------|
| **Mean** | 13.13 | 15.60 | 7.21 |
| **Median** | 13.00 | 14.00 | 6.00 |
| **Std Dev** | 6.38 | 9.64 | 6.10 |
| **Min** | 1 | 1 | 1 |
| **Max** | 44 | 468 | 82 |
| **25th %ile** | 8.00 | 10.00 | 3.00 |
| **75th %ile** | 17.00 | 20.00 | 10.00 |

### Key Observations:
- 🏆 Body elements are **most frequent** (avg 15.60 per image)
- 📝 Balloons are moderately frequent (avg 13.13 per image)
- 💬 Onomatopeia are least frequent (avg 7.21 per image)
- ⚠️ Body shows **highest variability** (max 468 per image!)

---

## 📏 3. Size Ratio Statistics (Segmentation-based)

*Percentage of total image area*

| Metric | Balloon | Body | Onomatopeia |
|--------|---------|------|-------------|
| **Mean** | 1.12% | 1.54% | 0.12% |
| **Median** | 0.88% | 0.85% | 0.04% |
| **Std Dev** | 0.98% | 2.17% | 0.25% |
| **Min** | 0.001% | 0.0001% | 0.0000% |
| **Max** | 37.12% | 86.52% | 7.55% |
| **25th %ile** | 0.54% | 0.41% | 0.012% |
| **75th %ile** | 1.40% | 1.77% | 0.11% |

### Key Observations:
- 🎯 Body elements occupy **largest average area** (1.54%)
- 💬 Balloons occupy moderate area (1.12%)
- ⚡ Onomatopeia are **very small** (0.12%, ~10× smaller)
- 📈 High variability in body sizes (max 86.52%)

---

## 📦 4. Bounding Box Size Ratio Statistics

*Percentage of total image area*

| Metric | Balloon | Body | Onomatopeia |
|--------|---------|------|-------------|
| **Mean** | 1.12% | 2.52% | 0.56% |
| **Median** | 0.88% | 1.41% | 0.15% |
| **Std Dev** | 0.98% | 3.57% | 1.42% |
| **Min** | 0.001% | 0.004% | 0.0001% |
| **Max** | 37.12% | 99.73% | 56.46% |
| **25th %ile** | 0.54% | 0.66% | 0.05% |
| **75th %ile** | 1.40% | 2.91% | 0.48% |

### Key Observations:
- 📦 Bounding boxes are larger than segmentation areas (as expected)
- 🎯 Body bounding boxes occupy **most space** (2.52% avg)
- ⚡ Onomatopeia bbox ~5× larger than segmentation

---

## 📐 5. Absolute Size Statistics (pixels)

### Area (pixels²)

| Metric | Balloon | Body | Onomatopeia |
|--------|---------|------|-------------|
| **Mean** | 22,139 | 30,254 | 2,299 |
| **Median** | 17,202 | 16,587 | 731 |
| **Std Dev** | 19,908 | 43,160 | 4,974 |
| **Min** | 52 | 1 | 1 |
| **Max** | 718,380 | 1,674,370 | 146,430 |

### Balloon Dimensions (pixels)

| Dimension | Mean | Median |
|-----------|------|--------|
| **Width** | 119 | 109 |
| **Height** | 167 | 157 |

### Key Observations:
- 🏆 Body elements are **largest** (avg 30,254 px²)
- 💬 Balloons are medium sized (avg 22,139 px²)
- ⚡ Onomatopeia are **smallest** (avg 2,299 px², ~13× smaller than balloons)

---

## 🔍 6. Comparative Analysis

### Relative Size Comparison
*Normalized to Balloon = 1.0*

| Metric | Balloon | Body | Onomatopeia |
|--------|---------|------|-------------|
| **Avg Area (segmentation)** | 1.00 | 1.37 | 0.11 |
| **Avg Area (bbox)** | 1.00 | 2.25 | 0.50 |
| **Avg Count per Image** | 1.00 | 1.19 | 0.55 |
| **Coverage %** | 1.00 | 1.02 | 0.85 |

### Efficiency Metrics
*Segmentation area / Bounding box area*

| Category | Fill Rate | Interpretation |
|----------|-----------|----------------|
| **Balloon** | 100.0% | 🟢 Tight bounding boxes |
| **Body** | 61.0% | 🟡 Partially filled boxes |
| **Onomatopeia** | 21.0% | 🔴 Sparse within boxes |

---

## 💡 7. Key Findings

### Distribution Characteristics
1. 🏆 **Body elements** are most prevalent (94.8% coverage) and largest on average
2. 💬 **Balloons** appear in 93.4% of images with moderate size
3. ⚡ **Onomatopeia** appear in 79.1% of images but are significantly smaller

### Size Characteristics
1. **Body elements:** Most variable (σ=2.17%), largest max size (86.52%)
2. **Balloons:** Consistent size (σ=0.98%), moderate coverage (1.12%)
3. **Onomatopeia:** Smallest and most compact (0.12% average)

### Spatial Efficiency
1. **Balloons** have tight bounding boxes (100% fill) ✅
2. **Body elements** partially fill bounding boxes (61% fill) ⚠️
3. **Onomatopeia** are sparse within bounding boxes (21% fill) ⚠️

### Typical Values (Medians)
| Category | Count/Image | % of Image | Area (px²) |
|----------|-------------|------------|------------|
| **Balloon** | 13 | 0.88% | 17,202 |
| **Body** | 14 | 0.85% | 16,587 |
| **Onomatopeia** | 6 | 0.04% | 731 |

---

## 🎓 8. Implications for Research

### Annotation Characteristics
- **Balloons and Body** have similar occurrence rates, but Body elements show much higher size variability, potentially making detection more challenging
- **Onomatopeia** are significantly smaller than other elements, requiring high-resolution processing or specialized small object detection techniques
- Categories with large gaps between segmentation and bounding box (Body, Onomatopeia) may benefit more from segmentation-based approaches

### Dataset Design Impact
- **Balloon Detection:** Relatively consistent size with dense annotations → standard object detection methods should work well
- **Body Detection:** High variability → scale-invariant methods and multi-scale processing are important
- **Onomatopeia Detection:** Extremely small objects → requires special training strategies (data augmentation, anchor size adjustment, etc.)

---

## 📁 Related Files

- English detailed reports:
  - `balloon_count_statistics.txt`
  - `balloon_bbox_statistics.txt`
  - `body_statistics.txt`
  - `onomatopeia_statistics.txt`

- Japanese detailed reports:
  - `balloon_count_statistics_jp.txt`
  - `balloon_bbox_statistics_jp.txt`
  - `body_statistics_jp.txt`
  - `onomatopeia_statistics_jp.txt`

- CSV data files:
  - `balloon_count_per_image.csv`
  - `body_per_image.csv`
  - `onomatopeia_per_image.csv`

---

**Generated:** 2025-11-04  
**Source:** Manga109 Dataset Analysis Pipeline
