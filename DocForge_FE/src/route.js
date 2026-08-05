import { createWebHistory } from "vue-router";
import { createRouter } from "vue-router";

const routes = [
    {
        path: "/",
        name: "home",
        component: () => import("./pages/client/Home.vue"),
    },
    // Giữ /convert cho link cũ / đã chia sẻ, tự chuyển sang công cụ mặc định
    {
        path: "/convert",
        redirect: "/convert/md-to-pdf",
    },
    {
        path: "/convert/md-to-pdf",
        name: "convert.md-to-pdf",
        component: () => import("./pages/client/ConvertPage.vue"),
    },
    // Thêm route khi từng công cụ được xây dựng — mỗi công cụ 1 page riêng,
    // dùng composable riêng theo khuôn useMdToPdfConverter() trong useApi.js.
    // {
    //     path: "/convert/pdf-to-word",
    //     name: "convert.pdf-to-word",
    //     component: () => import("./pages/client/PdfToWordPage.vue"),
    // },
    // {
    //     path: "/convert/pdf-to-md",
    //     name: "convert.pdf-to-md",
    //     component: () => import("./pages/client/PdfToMdPage.vue"),
    // },
    // {
    //     path: "/convert/word-to-pdf",
    //     name: "convert.word-to-pdf",
    //     component: () => import("./pages/client/WordToPdfPage.vue"),
    // },
    // {
    //     path: "/convert/word-to-md",
    //     name: "convert.word-to-md",
    //     component: () => import("./pages/client/WordToMdPage.vue"),
    // },
    // {
    //     path: "/convert/txt-to-md",
    //     name: "convert.txt-to-md",
    //     component: () => import("./pages/client/TxtToMdPage.vue"),
    // },

    // {
    //     path: "/car-details/:id",
    //     name: "car.details",
    //     component: () => import("./pages/client/CarDetails.vue"),
    // },
    // {
    //     path: "/car-list",
    //     name: "car.list",
    //     component: () => import("./pages/client/CarList.vue"),
    // }
    // {
    //     path: "/admin/danh-muc",
    //     name: "admin.category",
    //     component: () => import("./pages/admin/product_cate/List.vue"),
    // },
    // {
    //     path: "/admin/danh-muc/them-moi",
    //     name: "admin.category.create",
    //     component: () => import("./pages/admin/product_cate/Create.vue"),
    // },
    // {
    //     path: "/admin/danh-muc/sua/:id",
    //     name: "admin.category.edit",
    //     component: () => import("./pages/admin/product_cate/Edit.vue"),
    // },
    // {
    //     path: "/admin/san-pham/them-moi",
    //     name: "admin.product.create",
    //     component: () => import("./pages/admin/product/Create.vue")
    // },
    // {
    //     path: "/admin/san-pham",
    //     name: "admin.product.list",
    //     component: () => import("./pages/admin/product/List.vue")
    // },
    // {
    //     path: "/admin/san-pham/sua/:id",
    //     name: "admin.product.edit",
    //     component: () => import("./pages/admin/product/Edit.vue"),
    // },
    // {
    //     path: "/admin/danh-sach-don-hang",
    //     name: "admin.orders",
    //     component: () => import("./pages/admin/order/orders.vue")
    // },
    // {
    //     path: "/dang-ky",
    //     name: "register",
    //     component: () => import("./pages/account/Register.vue")
    // },
    // {
    //     path: "/dang-nhap",
    //     name: "login",
    //     component: () => import("./pages/account/Login.vue")
    // }
    // {
    //     path: "/gio-hang",
    //     name: "cart",
    //     component: () => import("./pages/client/Cart.vue")
    // },
    // {
    //     path: "/dat-hang",
    //     name: "checkout",
    //     component: () => import("./pages/client/Checkout.vue")
    // }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;