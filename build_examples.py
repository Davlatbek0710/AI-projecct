import json

INPUT_FILE = "dataset.txt"      
OUTPUT_FILE = "examples.json"   
CAPACITY = 400                  


def bins_from_order(order, capacity):
    bins = []
    cur = []
    s = 0
    for w in order:
        if s + w <= capacity:
            cur.append(w)
            s += w
        else:
            bins.append(cur)
            cur = [w]
            s = w
    if cur:
        bins.append(cur)
    return bins


def main():
    examples = []
    kept = 0
    skipped = 0

    with open(INPUT_FILE, "r", encoding="utf-8") as f_in:
        for line_no, line in enumerate(f_in, start=1):
            line = line.strip()
            if not line:
                continue

            parts = line.split("\t")

            
            capacity = int(parts[0])

            
            items = [int(x) for x in parts[1:11] if x]

            
            k_bins = int(parts[11])

            
            solution_order = [int(x) for x in parts[12:] if x]

            
            bins = bins_from_order(solution_order, capacity)

            
            if len(bins) != k_bins:
                print(
                    f"Skipping line {line_no}: k={k_bins}, "
                    f"in order becomes {len(bins)} bins"
                )
                skipped += 1
                continue

            
            bins_json = []
            for i, b in enumerate(bins, start=1):
                bins_json.append(
                    {
                        "id": i,
                        "items": b,
                        "load": sum(b),
                    }
                )

            assistant_answer = json.dumps({"bins": bins_json}, ensure_ascii=False)

            input_text = (
                f"Capacity: {capacity}. Items: " + ", ".join(map(str, items))
            )

            example = {
                "input": input_text,
                "answer": assistant_answer,
            }

            examples.append(example)
            kept += 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:
        json.dump(examples, f_out, ensure_ascii=False, indent=2)

    print(f"Ready. Saved samples: {kept}, skipped rows: {skipped}")


if __name__ == "__main__":
    main()